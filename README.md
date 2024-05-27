# API Service for MixedBread Embedding

-   Install requirements.txt
-   Additionally also install `torch`
-   Run the fast api app using `uvicorn app:app --reload`

## Deploy on Truefoundry

-   Login:
    `tfy login --host <Truefoundry Platform URL>`

-   Create a deploy.py file with the following content and add necessary details:

```python
from truefoundry.deploy import (
    Build,
    LocalSource,
    Port,
    DockerFileBuild,
    Service,
    Resources
)

service = Service(
    name="mixedbread-svc",

    # --- Build configuration i.e. How to package and build source code ---

    # This will instruct Truefoundry to automatically generate the Dockerfile and build it
    image=Build(
        build_source=LocalSource(local_build=False),
        build_spec=DockerFileBuild(dockerfile_path='./Dockerfile', command="uvicorn app:app --host 0.0.0.0 --port 8000")
    ),
    # Alternatively, you can use an already built public image of this codebase like follows:
    # image=Image(image_uri="truefoundrycloud/emotion-classification-fastapi:0.0.1")

    # --- Endpoints configuration i.e. How requests will reach the container ---

    ports=[
        Port(
            port=8000,
            # A model endpoint looks like https://{host}/{path}
            # Please see https://docs.truefoundry.com/docs/routing
            host="<Enter a host for the model endpoint>",
            path=None # <Enter optional path for model endpoint>,
        )
    ],

    # --- Environment Variables ---
    env={},

        # --- Resources ---
    resources=Resources(
        cpu_request=0.5, cpu_limit=1,
        memory_request=2000, memory_limit=4000,
        ephemeral_storage_request=1500, ephemeral_storage_limit=2000
    )
)

# Get your workspace fqn from https://docs.truefoundry.com/docs/workspace#copy-workspace-fqn-fully-qualified-name
service.deploy(workspace_fqn="<Enter Workspace FQN>", wait=False)
```
