
def env_check():
    try:
        import moxing as mox
        f'🎉 enviornment check pass: Modelarts enviornment checked'
        return True
    except:
        f'🎉 enviornment check failed: please run the code on the Qizhi platform NPU resource'
        return False

def dataset_to_env(multi_data_url, data_dir, unzip_required):
    if env_check():
        from .helper import moxing_dataset_to_env as func
        func(multi_data_url, data_dir, unzip_required)

def pretrain_to_env(pretrain_url, pretrain_dir):
    if env_check():
        from .helper import moxing_pretrain_to_env as func
        func(pretrain_url, pretrain_dir)

def obs_copy_file(obs_file_url, file_url):
    if env_check():
        from .helper import obs_copy_file as func
        func(obs_file_url, file_url)
    
def obs_copy_folder(folder_dir, obs_folder_url):
    if env_check():
        from .helper import obs_copy_folder as func
        func(folder_dir, obs_folder_url)

def upload_folder(folder_dir, obs_folder_url):
    if env_check():
        from .helper import upload_folder as func
        func(folder_dir, obs_folder_url)
        





       