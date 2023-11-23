# Pytorch Implementation of Contact Graspnet

This code is based heavily on 
https://github.com/alinasarmiento/pytorch_contactnet. Original Tensorflow implementation can be found at: https://github.com/NVlabs/contact_graspnet

Usage:

`import cgn_pytorch`

`cgn_model, optimizer, config_dict  = cgn_pytorch.from_pretrained()`

`cgn`

```
CGN(
  (set_abstract_msg): ModuleList(
    (0): ModuleList(
      (0): SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=3, out_features=32, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=32, out_features=32, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=32, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
      (1): SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=3, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=64, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=64, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
      (2): SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=3, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=64, out_features=96, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(96, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=96, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
    )
    (1): ModuleList(
      (0): SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=323, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=64, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=64, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
      (1-2): 2 x SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=323, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=128, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=128, out_features=256, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
    )
    (2): ModuleList(
      (0): SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=643, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=64, out_features=64, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=64, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
      (1-2): 2 x SAModule(
        (conv): PointNetConv(local_nn=Sequential(
          (0): Sequential(
            (0): Linear(in_features=643, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (1): Sequential(
            (0): Linear(in_features=128, out_features=128, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
          (2): Sequential(
            (0): Linear(in_features=128, out_features=256, bias=True)
            (1): ReLU()
            (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
          )
        ), global_nn=None)
      )
    )
  )
  (set_abstract_final): Sequential(
    (0): Sequential(
      (0): Linear(in_features=640, out_features=256, bias=True)
      (1): ReLU()
      (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    )
    (1): Sequential(
      (0): Linear(in_features=256, out_features=512, bias=True)
      (1): ReLU()
      (2): BatchNorm1d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    )
    (2): Sequential(
      (0): Linear(in_features=512, out_features=1024, bias=True)
      (1): ReLU()
      (2): BatchNorm1d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    )
  )
  (feat_prop): ModuleList(
    (0): FPModule(
      (nn): Sequential(
        (0): Sequential(
          (0): Linear(in_features=1280, out_features=256, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (1): Sequential(
          (0): Linear(in_features=256, out_features=256, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
    )
    (1): FPModule(
      (nn): Sequential(
        (0): Sequential(
          (0): Linear(in_features=896, out_features=256, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (1): Sequential(
          (0): Linear(in_features=256, out_features=128, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
    )
    (2): FPModule(
      (nn): Sequential(
        (0): Sequential(
          (0): Linear(in_features=448, out_features=128, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (1): Sequential(
          (0): Linear(in_features=128, out_features=128, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (2): Sequential(
          (0): Linear(in_features=128, out_features=128, bias=True)
          (1): ReLU()
          (2): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
      )
    )
  )
  (multihead): ModuleList(
    (0): Sequential(
      (0): Conv1d(131, 128, kernel_size=(1,), stride=(1,))
      (1): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (2): Dropout(p=0.5, inplace=False)
      (3): Conv1d(128, 1, kernel_size=(1,), stride=(1,))
    )
    (1-2): 2 x Sequential(
      (0): Conv1d(131, 128, kernel_size=(1,), stride=(1,))
      (1): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (2): Dropout(p=0.7, inplace=False)
      (3): Conv1d(128, 3, kernel_size=(1,), stride=(1,))
    )
    (3): Sequential(
      (0): Conv1d(131, 128, kernel_size=(1,), stride=(1,))
      (1): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (2): Dropout(p=0, inplace=False)
      (3): Conv1d(128, 1, kernel_size=(1,), stride=(1,))
    )
  )
  (success_sigmoid): Sigmoid()
  (width_relu): ReLU()
  (conf_loss_fn): BCEWithLogitsLoss()
)
```