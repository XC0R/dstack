# Quickstart

> Before using `dstack`, ensure you've [installed](installation/index.md) the server, or signed up for [dstack Sky :material-arrow-top-right-thin:{ .external }](https://sky.dstack.ai){:target="_blank"}.
    
## Initialize a repo

To use `dstack`'s CLI in a folder, first run [`dstack init`](reference/cli/index.md#dstack-init) within that folder.

<div class="termy">

```shell
$ mkdir quickstart && cd quickstart
$ dstack init
```

</div>

Your folder can be a regular local folder or a Git repo.

## Run a configuration

=== "Dev environment"

    A dev environment lets you provision an instance and access it with your desktop IDE.

    ##### Define a configuration

    Create the following configuration file inside the repo:

    <div editor-title=".dstack.yml"> 

    ```yaml
    type: dev-environment
    name: vscode
    
    # If `image` is not specified, dstack uses its default image
    python: "3.11"
    #image: dstackai/base:py3.13-0.6-cuda-12.1
    
    ide: vscode
    
    # Uncomment to request resources
    #resources:
    #  gpu: 24GB
    ```

    </div>

    ##### Run the configuration

    Run the configuration via [`dstack apply`](reference/cli/index.md#dstack-apply):

    <div class="termy">

    ```shell
    $ dstack apply -f .dstack.yml
    
     #  BACKEND  REGION           RESOURCES                 SPOT  PRICE
     1  gcp      us-west4         2xCPU, 8GB, 100GB (disk)  yes   $0.010052
     2  azure    westeurope       2xCPU, 8GB, 100GB (disk)  yes   $0.0132
     3  gcp      europe-central2  2xCPU, 8GB, 100GB (disk)  yes   $0.013248
     
    Submit the run vscode? [y/n]: y
    
    Launching `vscode`...
    ---> 100%
    
    To open in VS Code Desktop, use this link:
      vscode://vscode-remote/ssh-remote+vscode/workflow
    ```
    
    </div>

    Open the link to access the dev environment using your desktop IDE.

    Alternatively, you can access it via `ssh <run name>`.

=== "Task"

    A task allows you to schedule a job or run a web app. Tasks can be distributed and can forward ports.

    ##### Define a configuration

    Create the following configuration file inside the repo:

    <div editor-title="examples/misc/streamlit/serve-task.dstack.yml"> 

    ```yaml
    type: task
    name: streamlit
    
    # If `image` is not specified, dstack uses its default image
    python: "3.11"
    #image: dstackai/base:py3.13-0.6-cuda-12.1
    
    # Commands of the task
    commands:
      - pip install streamlit
      - streamlit hello
    # Ports to forward
    ports:
      - 8501

    # Uncomment to request resources
    #resources:
    #  gpu: 24GB
    ```

    </div>

    By default, tasks run on a single instance. To run a distributed task, specify 
    [`nodes` and system environment variables](reference/dstack.yml/task.md#distributed-tasks), 
    and `dstack` will run it on a cluster.

    ##### Run the configuration

    Run the configuration via [`dstack apply`](reference/cli/index.md#dstack-apply):

    <div class="termy">

    ```shell
    $ dstack apply -f streamlit.dstack.yml
    
     #  BACKEND  REGION           RESOURCES                 SPOT  PRICE
     1  gcp      us-west4         2xCPU, 8GB, 100GB (disk)  yes   $0.010052
     2  azure    westeurope       2xCPU, 8GB, 100GB (disk)  yes   $0.0132
     3  gcp      europe-central2  2xCPU, 8GB, 100GB (disk)  yes   $0.013248
     
    Submit the run streamlit? [y/n]: y
     
    Continue? [y/n]: y
    
    Provisioning `streamlit`...
    ---> 100%

      Welcome to Streamlit. Check out our demo in your browser.

      Local URL: http://localhost:8501
    ```
    
    </div>

    If you specified `ports`, they will be automatically forwarded to `localhost` for convenient access.

=== "Service"

    A service allows you to deploy a model or any web app as an endpoint.

    ##### Define a configuration

    Create the following configuration file inside the repo:

    <div editor-title="examples/deployment/vllm/service.dstack.yml"> 

    ```yaml
    type: service
    name: llama31-service
    
    # If `image` is not specified, dstack uses its default image
    python: "3.11"
    #image: dstackai/base:py3.13-0.6-cuda-12.1
    
    # Required environment variables
    env:
      - HF_TOKEN
    commands:
      - pip install vllm
      - vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --max-model-len 4096
    # Expose the vllm server port
    port: 8000

    # Specify a name if it's an Open-AI compatible model
    model: meta-llama/Meta-Llama-3.1-8B-Instruct
    
    # Required resources
    resources:
      gpu: 24GB
    ```

    </div>

    ##### Run the configuration

    Run the configuration via [`dstack apply`](reference/cli/index.md#dstack-apply):

    <div class="termy">

    ```shell
    $ dstack apply -f streamlit.dstack.yml
    
     #  BACKEND  REGION           RESOURCES                 SPOT  PRICE
     1  gcp      us-west4         2xCPU, 8GB, 100GB (disk)  yes   $0.010052
     2  azure    westeurope       2xCPU, 8GB, 100GB (disk)  yes   $0.0132
     3  gcp      europe-central2  2xCPU, 8GB, 100GB (disk)  yes   $0.013248
     
    Submit the run streamlit? [y/n]: y
     
    Continue? [y/n]: y
    
    Provisioning `streamlit`...
    ---> 100%

    Service is published at: 
      http://localhost:3000/proxy/services/main/llama31-service
    ```
    
    </div>

    If you specified `model`, the model will also be available via an OpenAI-compatible endpoint at
    `<dstack server URL>/proxy/models/<project name>`.

    ??? info "Gateway"
        By default, services run on a single instance. However, you can specify `replicas` and `target` to enable 
        [auto-scaling](reference/dstack.yml/service.md#auto-scaling).

        Note, to use auto-scaling, a custom domain, or HTTPS, set up a 
        [gateway](concepts/gateways.md) before running the service.
        A gateway pre-configured for you if you are using [dstack Sky :material-arrow-top-right-thin:{ .external }](https://sky.dstack.ai){:target="_blank"}.

`dstack apply` automatically provisions instances, uploads the code from the current repo (incl. your local uncommitted changes).

## Troubleshooting

Something not working? See the [troubleshooting](guides/troubleshooting.md) guide.

## What's next?

1. Read about [dev environments](dev-environments.md), [tasks](tasks.md), 
    [services](services.md), and [fleets](concepts/fleets.md) 
2. Join [Discord :material-arrow-top-right-thin:{ .external }](https://discord.gg/u8SmfwPpMd)
3. Browse [examples](https://dstack.ai/examples)
