"""
Author: Radek Danecek
Copyright (c) 2022, Radek Danecek
All rights reserved.

# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# Using this computer program means that you agree to the terms 
# in the LICENSE file included with this software distribution. 
# Any use not explicitly granted by the LICENSE is prohibited.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# For comments or questions, please email us at emoca@tue.mpg.de
# For commercial licensing contact, please contact ps-license@tuebingen.mpg.de
"""


from gdl.utils.condor import execute_on_cluster
from pathlib import Path
import affectnet_validation as script
import datetime
from omegaconf import OmegaConf
import time as t

def submit(cfg, model_folder_name, mode, bid=10):
    cluster_repo_path = "/home/rdanecek/workspace/repos/gdl"
    # submission_dir_local_mount = "/home/rdanecek/Workspace/mount/scratch/rdanecek/emoca/submission"
    submission_dir_local_mount = "/is/cluster/work/rdanecek/emoca/affectnet_test_submission"
    # submission_dir_cluster_side = "/ps/scratch/rdanecek/emoca/submission"
    submission_dir_cluster_side = "/is/cluster/work/rdanecek/emoca/affectnet_test_submission"
    time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    submission_folder_name = time + "_" + "submission"
    submission_folder_local = Path(submission_dir_local_mount) / submission_folder_name
    submission_folder_cluster = Path(submission_dir_cluster_side) / submission_folder_name

    local_script_path = Path(script.__file__).absolute()
    cluster_script_path = Path(cluster_repo_path) / local_script_path.parents[1].name \
                          / local_script_path.parents[0].name / local_script_path.name

    submission_folder_local.mkdir(parents=True)

    # python_bin = 'python'
    python_bin = '/home/rdanecek/anaconda3/envs/<<ENV>>/bin/python'
    username = 'rdanecek'
    gpu_mem_requirement_mb = cfg.detail.learning.gpu_memory_min_gb * 1024
    # gpu_mem_requirement_mb = None
    # cpus = cfg.detail.data.num_workers + 2 # 1 for the training script, 1 for wandb or other loggers (and other stuff), the rest of data loading
    cpus = 2 # 1 for the training script, 1 for wandb or other loggers (and other stuff), the rest of data loading
    gpus = cfg.detail.learning.num_gpus
    num_jobs = 1
    max_time_h = 10
    max_price = 8000
    job_name = "finetune_deca"
    cuda_capability_requirement = 7
    mem_gb = 12
    args = f"{model_folder_name} {mode}"

    execute_on_cluster(str(cluster_script_path),
                       args,
                       str(submission_folder_local),
                       str(submission_folder_cluster),
                       str(cluster_repo_path),
                       python_bin=python_bin,
                       username=username,
                       gpu_mem_requirement_mb=gpu_mem_requirement_mb,
                       cpus=cpus,
                       mem_gb=mem_gb,
                       gpus=gpus,
                       num_jobs=num_jobs,
                       bid=bid,
                       max_time_h=max_time_h,
                       max_price=max_price,
                       job_name=job_name,
                       cuda_capability_requirement=cuda_capability_requirement,
                       max_concurrent_jobs = 15,
                       concurrency_tag = "af_test",
                       modules_to_load=['cuda/11.4'],
                       )
    t.sleep(1)

def main():
    # path_to_models = '/home/rdanecek/Workspace/mount/scratch/rdanecek/emoca/finetune_deca'
    # path_to_models = '/ps/scratch/rdanecek/emoca/finetune_deca'
    path_to_models = '/is/cluster/work/rdanecek/emoca/finetune_deca'

    run_names = []
    # run_names += ['2021_03_25_19-42-13_DECA_training'] # EMOCA EmoNet
    # run_names += ['2021_03_29_23-14-42_DECA__EmoLossB_F2VAEw-0.00150_DeSegFalse_early'] # EMOCA EmoNet
    # run_names += ['2021_03_18_21-10-25_DECA_training'] # Basic EMOCA
    # run_names += ['2021_03_26_15-05-56_DECA__DeSegFalse_DwC_early'] # Detail with coarse
    # run_names += ['2021_03_26_14-36-03_DECA__DeSegFalse_DeNone_early'] # No detail exchange

    # aff-wild 2 fintuned models
    # run_names += ['2021_04_02_18-46-31_va_DeSegFalse_Aug_early'] # EMOCA
    # run_names += ['2021_04_02_18-46-47_va_EmoLossB_F2VAEw-0.00150_DeSegFalse_Aug_early'] # EMOCA with EmoNet
    # run_names += ['2021_04_02_18-46-34_va_DeSegFalse_Aug_DwC_early'] # EMOCA detail with coarse
    # run_names += ['2021_04_02_18-46-51_va_DeSegFalse_DeNone_Aug_DwC_early'] # EMOCA detail with coarse , no exchange

    ## ExpDeca ablations
    ## Deca set
    # run_names += ['2021_04_19_18-57-31_ExpDECA_DecaD_para_Jaw_NoRing_DeSegrend_early'] # ran
    # run_names += ['2021_04_19_18-57-50_ExpDECA_DecaD_para_Jaw_NoRing_DeSegrendNoLmk_DwC_early'] # ran
    # run_names += ['2021_04_19_18-57-53_ExpDECA_DecaD_para_Jaw_NoRing_DeSegrend_DwC_early'] # ran
    # run_names += ['2021_04_19_18-58-27_ExpDECA_DecaD_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrendNoLmk_DwC_early'] # ran
    # run_names += ['2021_04_20_19-09-37_ExpDECA_DecaD_EmoTrain_Jaw_NoRing_DeSegrend_early'] # ran
    # run_names += ['2021_04_20_19-09-44_ExpDECA_DecaD_clone_Jaw_NoRing_DeSegrend_early'] # ran
    # run_names += ['2021_04_20_19-10-57_ExpDECA_DecaD_para_Jaw_DeSegrend_early'] ## ran
    # run_names += ['2021_04_19_18-55-46_ExpDECA_DecaD_EmoStat_Jaw_NoRing_DeSegrend_early'] # ran
    ## run_names += ['2021_04_23_10-35-48_ExpDECA_DecaD_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_early'] ## stil running

    # # AffectNet
    # run_names += ['2021_04_19_18-58-39_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_early'] # ran
    # run_names += ['2021_04_19_18-58-40_ExpDECA_Affec_para_Jaw_NoRing_DeSegrendNoLmk_DwC_early'] # ran
    # run_names += ['2021_04_19_18-59-02_ExpDECA_Affec_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_early'] ### ran
    # run_names += ['2021_04_19_18-59-19_ExpDECA_Affec_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_DwC_early'] # ran
    # run_names += ['2021_04_19_19-04-35_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_DwC_early'] ## ran
    # run_names += ['2021_04_19_19-05-43_ExpDECA_Affec_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrendNoLmk_DwC_early'] # ran
    # run_names += ['2021_04_20_21-39-59_ExpDECA_Affec_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_early']  ### ran
    # run_names += ['2021_04_20_18-36-33_ExpDECA_Affec_para_Jaw_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_DwC_early']  ### ran
    # run_names += ['2021_04_19_18-56-08_ExpDECA_Affec_EmoStat_Jaw_NoRing_DeSegrend_early']  ## ran

    ### EMOCA no ring ablations
    # # Deca set
    # run_names += ['2021_04_23_17-06-29_ExpDECA_DecaD_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_DwC_early'] # ran
    # run_names += ['2021_04_23_17-05-49_ExpDECA_DecaD_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_early']  # ran
    # run_names += ['2021_04_23_17-00-40_ExpDECA_DecaD_NoRing_DeSegrend_early']  # ran
    # # run_names += ['']
    #
    # # AffectNet
    # run_names += ['2021_04_23_17-12-20_DECA_Affec_NoRing_DeSegrend_DwC_early']  # ran
    # run_names += ['2021_04_23_17-12-05_DECA_Affec_NoRing_DeSegrend_early']  # ran
    # run_names += ['2021_04_23_17-11-08_DECA_Affec_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_DwC_early']  # ran
    # run_names += ['2021_04_23_17-10-53_DECA_Affec_NoRing_EmoLossB_F2VAEw-0.00150_DeSegrend_early'] # ran


    ### ExpDECA expression rings
    # geometric expression rings - these need a few more days of finetuning
    # run_names += ['2021_05_07_20-48-30_ExpDECA_Affec_para_Jaw_EmoB_F2VAE_GeEx_DeSegrend_BlackB_Exgt_va_CoNone_DeNone_DwC_early']
    # run_names += ['2021_05_07_20-46-09_ExpDECA_Affec_para_Jaw_EmoB_F2VAE_GeEx_DeSegrend_BlackB_Exgt_va_CoNone_DeNone_early']
    # run_names += ['2021_05_07_20-45-33_ExpDECA_Affec_para_Jaw_EmoB_F2VAE_GeEx_DeSegrend_BlackB_Exemonet_feature_CoNone_DeNone_DwC_early']
    # run_names += ['2021_05_07_20-36-43_ExpDECA_Affec_para_Jaw_EmoB_F2VAE_GeEx_DeSegrend_BlackB_Exemonet_feature_CoNone_DeNone_early']

    # only emotion expression rings
    # run_names += ['2021_05_02_12-43-06_ExpDECA_Affec_para_Jaw_EmoLossB_F2VAEw-0.00150_DeSegrend_BlackB_Exgt_expression_CoNone_DeNone_early'] # ran
    # run_names += ['2021_05_02_12-42-01_ExpDECA_Affec_para_Jaw_EmoLossB_F2VAEw-0.00150_DeSegrend_BlackB_Exemonet_feature_CoNone_DeNone_DwC_early'] # ran
    # run_names += ['2021_05_02_12-37-20_ExpDECA_Affec_para_Jaw_EmoLossB_F2VAEw-0.00150_DeSegrend_BlackB_Exgt_expression_CoNone_DeNone_DwC_early'] # ran
    # run_names += ['2021_05_02_12-36-00_ExpDECA_Affec_para_Jaw_EmoLossB_F2VAEw-0.00150_DeSegrend_BlackB_Exgt_va_CoNone_DeNone_DwC_early'] # ran
    # run_names += ['2021_05_02_12-35-44_ExpDECA_Affec_para_Jaw_EmoLossB_F2VAEw-0.00150_DeSegrend_BlackB_Exgt_va_CoNone_DeNone_early'] # ran
    # run_names += ['2021_05_02_12-34-47_ExpDECA_Affec_para_Jaw_EmoLossB_F2VAEw-0.00150_DeSegrend_BlackB_Exemonet_feature_CoNone_DeNone_early'] # ran

    ### ExpDECA with EmoMLP
    # run_names += ['2021_05_21_15-44-46_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.1_early']
    # run_names += ['2021_05_21_15-44-48_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.5_early']
    # run_names += ['2021_05_21_15-44-49_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.05_early']
    # run_names += ['2021_05_21_15-44-45_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.005_early'] # TO BE RAN

    ### ExpDECA DwC with EmoMLP
    # run_names += ['2021_05_24_12-22-17_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.1_DwC_early']
    # run_names += ['2021_05_24_12-22-17_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.05_DwC_early'] # TO BE RAN
    # # run_names += ['2021_05_24_12-22-21_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.005_DwC_early'] # TO BE RAN
    # run_names += ['2021_05_24_12-21-45_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_0.5_DwC_early'] # TO BE RAN

    # # ExpDECA DwC with (semi)detached MLP
    # run_names += ['2021_06_01_15-11-07_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_1.0_detEJ_DwC_early']
    # run_names += ['2021_06_01_15-09-16_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_1.0_detEDJ_DwC_early']
    # run_names += ['2021_06_01_15-04-45_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_1.0_detD_DwC_early']
    # run_names += ['2021_06_01_15-04-05_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_1.0_detDJ_DwC_early']
    # run_names += ['2021_06_01_15-02-35_ExpDECA_Affec_para_Jaw_NoRing_DeSegrend_Exnone_MLP_1.0_detJ_DwC_early']


    # ExpDECA STAR (with neural rendering) # run later
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_24_00-13-33_ExpDECAStar_Affec_para_Jaw_EmoB_F2VAE_DeSegrend_Exnone_DeNo_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-51-44_ExpDECAStar_Affec_para_Jaw_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Exnone_DeNo_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-51-58_ExpDECAStar_Affec_para_Jaw_NoRing_EmoB_EmoNet_sha_F2VAE_DeSegrend_Exnone_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-51-59_ExpDECAStar_Affec_para_Jaw_NoRing_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Exnone_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-52-13_ExpDECAStar_Affec_para_Jaw_EmoB_EmoCnn_res_F2VAE_DeSegrend_Exnone_DeNo_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-52-13_ExpDECAStar_Affec_para_Jaw_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Exnone_DeNo_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-52-18_ExpDECAStar_Affec_para_Jaw_NoRing_EmoB_EmoCnn_res_F2VAE_DeSegrend_Exnone_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-52-29_ExpDECAStar_Affec_para_Jaw_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Exnone_DeNo_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-52-30_ExpDECAStar_Affec_para_Jaw_NoRing_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Exnone_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_26_10-52-43_ExpDECAStar_Affec_para_Jaw_NoRing_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Exnone_DwC_early']


    # ExpDECA with different emotion networks (coarse and detail separate), uniform sampling
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_31_12-33-29_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Aug_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_31_12-33-26_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Aug_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_31_12-33-07_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoCnn_res_F2VAE_DeSegrend_Aug_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_31_12-32-41_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Aug_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_31_12-32-20_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Aug_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_08_31_12-30-25_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoNet_sha_F2VAE_DeSegrend_Aug_early']

    # # ExpDECA with different emotion networks (coarse and detail separate), expression-balanced sampling
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_03_15-04-12_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Aug_early/']
    #
    # # ExpDECA with different emotion networks (coarse and detail+coarse), expression-balanced sampling
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_03_10-22-52_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Aug_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_03_10-21-57_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoNet_sha_F2VAE_DeSegrend_Aug_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_03_10-21-45_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Aug_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_02_23-05-07_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoSwin_sw_F2VAE_DeSegrend_Aug_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_02_23-02-48_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoCnn_res_F2VAE_DeSegrend_Aug_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_02_23-00-53_ExpDECA_Affec_para_Jaw_NoRing_EmoB_EmoCnn_vgg_F2VAE_DeSegrend_Aug_DwC_early']
    #
    #
    # # ExpDECA with trainable dual emotion network
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_04_22-00-22_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early']
    # run_names += ['/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_04_22-00-04_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early']

    #
    # # ExpDECA with trainable dual emotion network, cosine similarity
    #
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_21-14-14_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2ncosVAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_21-13-44_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2ncosVAE_DeSegrend_Aug_early"]
    #
    # # ExpDECA with trainable dual emotion network, emo loss but features are normalized before computing loss
    #
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_21-13-42_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2nVAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_21-13-32_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2nVAE_DeSegrend_Aug_early"]

    ## ExpDECA with trainable dual emotion network, different emo loss weights
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-36_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-35_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-26_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-25_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-15_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-13_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-12_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-12_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-09_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-08_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-19-08_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-10-49_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_VGGl_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_07_19-10-36_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_VGGl_EmoB_EmoCnn_vgg_du_F2VAE_DeSegrend_Aug_early"]

    # ExpDECA with  AU supervision
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_10_11-04-25_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AUf-cos_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-33-31_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-33-15_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-33-10_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_10_11-04-42_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AUf-cos_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-25-29_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-25-29_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_EmoB_EmoCnn_vgg_du_F2VAE_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-25-08_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-24-47_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-45_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-41_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-41_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-39_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-38_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-37_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-35_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-35_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-25_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-23-24_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-20-59_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_DwC_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_09_09_15-20-32_ExpDECA_Affec_balanced_expr_para_Jaw_NoRing_AU_DeSegrend_Aug_early"]

    mode = 'coarse'
    # mode = 'detail'


    # # ExpDECA with stronger emonet loss withouth jaw
    ## run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-59-10_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-58-28_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-58-11_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-55-47_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-55-25_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-55-14_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-55-12_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-54-31_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-53-48_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-53-44_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_10-50-22_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_15-02-19_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-59-51_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-59-38_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-59-25_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-57-14_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-57-09_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-52-01_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-52-00_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-09-55_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-09-45_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-09-16_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_27_14-09-02_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_11-58-32_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_11-57-47_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_11-56-07_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_18-54-54_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_18-54-45_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_18-53-53_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_18-30-31_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_18-30-14_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_10-18-37_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_10-18-18_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_25_10-18-05_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_22_12-23-05_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_22_12-23-04_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_22_12-23-03_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_22_10-38-21_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    #
    #Barlow Twins
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_22-41-34_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_22-39-54_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_22-39-46_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_22-39-42_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_11-22-58_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_11-19-45_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_11-19-20_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_11-19-17_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_28_11-19-10_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]

    # other emotion networks
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_29_22-23-28_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_29_22-23-25_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]

    # # AU loss
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_13-46-06_ExpDECA_Affec_clone_NoRing_AUf-cos_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_13-37-57_ExpDECA_Affec_clone_NoRing_AUf-cos_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_13-22-46_ExpDECA_Affec_clone_NoRing_AUf-cos_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_13-17-11_ExpDECA_Affec_clone_NoRing_AUf-cos_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_13-17-10_ExpDECA_Affec_clone_NoRing_AUf-cos_DeSegrend_BlackB_Aug_early"]

    # ## on EMOCA Dataset ( sth might wrong and be badly trained here, not sure )
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_15-08-44_ExpDECA_DecaD_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_13-15-16_ExpDECA_DecaD_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_12-35-21_ExpDECA_DecaD_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_26_12-29-38_ExpDECA_DecaD_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]

    # para architecture
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_29_21-30-28_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_29_21-34-01_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_29_22-01-32_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_29_22-01-40_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    #
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_30_20-50-53_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_30_20-50-54_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_30_20-48-16_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_30_20-47-54_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_30_20-47-47_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_10_30_20-33-39_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]


    # # final ResNet sweep
    # # run_names += [
    # #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-24_7057622275122671174_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-06_-6506673705064889607_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-06_-1007531484471246016_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-03_480128111237298530_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-03_-3847743713390055217_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-01_7226661150207254923_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-01_7193545667483921831_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-41-01_-7746686909198123775_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-59_-6970716391423648964_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-59_-4293993865315558856_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-54_-8956728687580574108_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-52_3535801695749609832_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-52_-776769225150723181_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-48_-3557093149321491446_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-48_-1130509047528431540_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-45_6758302146806216456_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-33_8529519700345615983_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-33_7640188424869169886_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-27_4344460465829536839_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-27_6877124675180108840_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-03_-8436446076366773310_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-03_-4636033309105620245_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-02_833576158064688874_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-40-02_8285199837830669798_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    #
    # # final SWIN sweep
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_03_02-20-54_-1968661455773213379_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_03_02-42-36_2407313258403191383_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-12-49_-2741982989276466203_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-10-49_1731595146375171932_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-10-49_-7667543226652993592_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-10-40_6872394600987091012_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-10-40_-8572124953572605249_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-10-40_-7473769445402844399_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_13-10-40_-5241005287738579855_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-54-01_2637759665938415282_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_5168561227047398084_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_2319744141436125537_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_2073066276032009236_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_-6306367650010438382_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_-3218674826605317504_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_-1846739961689335557_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-47-35_-1022988189955888024_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-55_5806971874713117653_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-55_-5348873875193364241_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-54_-7598613731487617091_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-45_5490409369290264125_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-45_1092553962037855966_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-43_2271671740894586800_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-43_-5593491350755409121_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-41_4316282956709408142_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_02_12-42-41_-1213070571142271333_ExpDECA_Affec_para_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]

    # run_names +=[ # mturk resnet model
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236352_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early/"
    # ]

    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/" \
    #               "2021_11_13_03-43-40_4753326650554236353_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering"]
    # run_names += ["is/cluster/work/rdanecek/emoca/finetune_deca/"
    #               "2021_11_13_03-43-40_4753326650554236354_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering_not_blurred"]

    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236354_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering_not_blurred"]

    # run_names += [
    #     "/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236354_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering_not_blurred"
    # ]

    # 
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236358_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering_not_blurred_5"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236359_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering_not_blurred_4"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236360_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering_not_blurred_3"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236357_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering5"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236356_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering4"]
    # # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_13_03-43-40_4753326650554236355_ExpDECA_Affec_clone_NoRing_EmoC_F2_DeSeggt_BlackC_Aug_early_masked_rendering3"]


    # emonet weight ablation visuals 
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_09_19-00-11_1056504990304470492_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_09_19-04-15_9157589239172551865_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_09_19-04-15_9157589239172551865_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_09_19-00-11_1056504990304470492_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]
    # run_names += ["/is/cluster/work/rdanecek/emoca/finetune_deca/2021_11_09_19-00-11_-3505404531826926943_ExpDECA_Affec_clone_NoRing_EmoB_F2_DeSegrend_BlackB_Aug_early"]



    for run_name in run_names:
        run_path = Path(path_to_models) / run_name
        with open(Path(run_path) / "cfg.yaml", "r") as f:
            conf = OmegaConf.load(f)
        submit(conf, run_name, mode)


if __name__ == "__main__":
    main()
