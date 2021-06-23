import sys

import torch
import pytorch_lightning as pl
import numpy as np
from utils.other import class_from_str
import torch.nn.functional as F
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.loggers import WandbLogger
from datasets.AffectNetDataModule import AffectNetExpressions
from datasets.FaceVideoDataset import Expression7
from pathlib import Path
from utils.lightning_logging import _log_array_image, _log_wandb_image, _torch_image2np
from models.EmotionRecognitionModuleBase import EmotionRecognitionBaseModule
from omegaconf import open_dict
from .Swin import create_swin_backbone

class EmoSwinModule(EmotionRecognitionBaseModule):

    def __init__(self, config):
        super().__init__(config)
        self.n_expression = 9  # we use all affectnet classes (included none) for now
        with open_dict(config.model.swin_cfg):
            self.swin = create_swin_backbone(config.model.swin_cfg,
                                             self.n_expression + 2,
                                             config.data.image_size,
                                             config.model.load_pretrained_swin,
                                             self.config.model.swin_type )

        self.num_classes = self.n_expression

    def forward_swin(self, images):
        output = self.swin(images)

        out_idx = 0
        if self.config.model.predict_expression:
            expr_classification = output[:, out_idx:(out_idx + self.num_classes)]
            if self.exp_activation is not None:
                expr_classification = self.exp_activation(output[:, out_idx:(out_idx + self.num_classes)], dim=1)
            out_idx += self.num_classes
        else:
            expr_classification = None

        if self.config.model.predict_valence:
            valence = output[:, out_idx:(out_idx + 1)]
            if self.v_activation is not None:
                valence = self.v_activation(valence)
            out_idx += 1
        else:
            valence = None

        if self.config.model.predict_arousal:
            arousal = output[:, out_idx:(out_idx + 1)]
            if self.a_activation is not None:
                arousal = self.a_activation(output[:, out_idx:(out_idx + 1)])
            out_idx += 1
        else:
            arousal = None

        values = {}
        values["valence"] = valence
        values["arousal"] = arousal
        values["expr_classification"] = expr_classification
        return values


    def forward(self, batch):
        images = batch['image']

        if len(images.shape) == 5:
            K = images.shape[1]
        elif len(images.shape) == 4:
            K = 1
        else:
            raise RuntimeError("Invalid image batch dimensions.")

        # print("Batch size!")
        # print(images.shape)
        images = images.view(-1, images.shape[-3], images.shape[-2], images.shape[-1])

        emotion = self.forward_swin(images)

        valence = emotion['valence']
        arousal = emotion['arousal']

        # emotion['expression'] = emotion['expression']

        # classes_probs = F.softmax(emotion['expression'])
        expression = self.exp_activation(emotion['expr_classification'], dim=1)

        values = {}
        values['valence'] = valence.view(-1,1)
        values['arousal'] = arousal.view(-1,1)
        values['expr_classification'] = expression

        # TODO: WARNING: HACK
        if self.n_expression == 8:
            values['expr_classification'] = torch.cat([
                values['expr_classification'], torch.zeros_like(values['expr_classification'][:, 0:1])
                                               + 2*values['expr_classification'].min()],
                dim=1)

        return values

    def _get_trainable_parameters(self):
        return list(self.swin.parameters())

    ## we can leave the default implementation
    # def train(self, mode=True):
    #     pass

    def _vae_2_str(self, valence=None, arousal=None, affnet_expr=None, expr7=None, prefix=""):
        caption = ""
        if len(prefix) > 0:
            prefix += "_"
        if valence is not None and not np.isnan(valence).any():
            caption += prefix + "valence= %.03f\n" % valence
        if arousal is not None and not np.isnan(arousal).any():
            caption += prefix + "arousal= %.03f\n" % arousal
        if affnet_expr is not None and not np.isnan(affnet_expr).any():
            caption += prefix + "expression= %s \n" % AffectNetExpressions(affnet_expr).name
        if expr7 is not None and not np.isnan(expr7).any():
            caption += prefix +"expression= %s \n" % Expression7(expr7).name
        return caption

    def _test_visualization(self, output_values, input_batch, batch_idx, dataloader_idx=None):
        batch_size = input_batch['image'].shape[0]

        visdict = {}
        if 'image' in input_batch.keys():
            visdict['inputs'] = input_batch['image']

        valence_pred = output_values["valence"]
        arousal_pred = output_values["arousal"]
        expr_classification_pred = output_values["expr_classification"]

        valence_gt = input_batch["va"][:, 0:1]
        arousal_gt = input_batch["va"][:, 1:2]
        expr_classification_gt = input_batch["affectnetexp"]

        # visdict = self.deca._create_visualizations_to_log("test", visdict, output_values, batch_idx,
        #                                                   indices=0, dataloader_idx=dataloader_idx)

        if isinstance(self.logger, WandbLogger):
            caption = self._vae_2_str(
                valence=valence_pred.detach().cpu().numpy(),
                arousal=arousal_pred.detach().cpu().numpy(),
                affnet_expr=torch.argmax(expr_classification_pred).detach().cpu().numpy().astype(np.int32),
                expr7=None, prefix="pred")
            caption += self._vae_2_str(
                valence=valence_gt.cpu().numpy(),
                arousal=arousal_gt.cpu().numpy(),
                affnet_expr=expr_classification_gt.cpu().numpy().astype(np.int32),
                expr7=None, prefix="gt")


        stage = "test"
        vis_dict = {}

        i = 0 # index of sample in batch to log
        for key in visdict.keys():
            images = _torch_image2np(visdict[key])
            savepath = Path(
                f'{self.config.inout.full_run_dir}/{stage}/{key}/{self.current_epoch:04d}_{batch_idx:04d}_{i:02d}.png')
            image = images[i]
            # im2log = Image(image, caption=caption)
            if isinstance(self.logger, WandbLogger):
                im2log = _log_wandb_image(savepath, image, caption)
            elif self.logger is not None:
                im2log = _log_array_image(savepath, image, caption)
            else:
                im2log = _log_array_image(None, image, caption)
            name = stage + "_" + key
            if dataloader_idx is not None:
                name += "/dataloader_idx_" + str(dataloader_idx)
            vis_dict[name] = im2log

        if isinstance(self.logger, WandbLogger):
            self.logger.log_metrics(vis_dict)
        return vis_dict