# Graph Database

Synthetic graph database generation. Each class is generated with a prototype and afterwards distortions are applied.

    $ pip install -r requirements.txt
    $ python generate_dataset.py --dirPrototypes ['./prototypes/Letters/'] --nodeThreshold 0.4  
       --dirDataset './dataset/Letters/' --division (5000, 3000, 3000)
    
## Add nodes

Controlled by __--nodeThreshold__ parameter, increase the number of nodes of the prototypes before the deformation. It tries to add a node at the specified distance, equispaced following the edges.

Some examples with graph A normalized before and after adding the nodes:

|Original graph |
| ------------- |
|<img src="https://github.com/priba/graph_db/blob/master/readme_plots/A.png" width="200">|

| --nodeThreshold  | Image | | --nodeThreshold  | Image |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| 0.1  | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_01.png" width="200"> | | 0.2 | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_02.png" width="200"> |
| 0.3  | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_03.png" width="200"> | | 0.4 | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_04.png" width="200"> |

## Node distortion

Controlled by __--nodeDisplace__ parameter, add random noise following a normal distribution center at each node with standard deviation set by --nodeDisplace.

Some examples with graph A where --nodeThreshold has been set to 0.4.

|Original graph |
| ------------- |
|<img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_04.png" width="200">|

| --nodeDisplace  | Image | | --nodeDisplace  | Image |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| 0.01  | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_04_001.png" width="200"> | | 0.05 | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_04_005.png" width="200"> |
| 0.1   | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_04_01.png" width="200"> | | 0.2 | <img src="https://github.com/priba/graph_db/blob/master/readme_plots/A_04_02.png" width="200"> |
