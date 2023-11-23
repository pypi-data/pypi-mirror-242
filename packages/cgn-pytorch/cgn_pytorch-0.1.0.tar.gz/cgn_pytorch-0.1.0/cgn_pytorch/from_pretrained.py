import torch

from cgn_pytorch import CGN
import cgn_pytorch.util.config_utils as config_utils


def initialize_net(config_file, load_model, save_path):
    print('initializing net')
    torch.cuda.empty_cache()
    config_dict = config_utils.load_config(config_file)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = CGN(config_dict, device).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    if load_model:
        print('loading model')
        checkpoint = torch.load(save_path, map_location=device)
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])

    return model, optimizer, config_dict
