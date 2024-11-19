.PHONY: image run bash shell push-labacr

help:
	@echo "available make commands"
	@echo "make image        - build image from Dockerfile, tagged 'oahpa_all'"
	@echo "make run          - run oahpa_all, serving on port 80"
	@echo "make runlocal     - run oahpa_all, serving on port 5000"
	@echo "make run-bash     - run oahpa_all, but run bash instead of supervisord"
	@echo "make shell        - start bash in the running oahpa_all container"
	@echo "make push-labacr  - tag and push to gtlabcontainerregistry.azurecr.io"

image:
	podman build -t oahpa_all -f Dockerfile ..

run:
	podman run --rm --name oahpa_all -p 5000:80 oahpa_all

runlocal:
	podman run --rm --name oahpa_all -v ./smi:/opt/smi -p 5002:80 oahpa_all

run-bash:
	podman run --rm -it oahpa_all bash

shell:
	podman exec -it oahpa_all bash

push-labacr:
	podman tag oahpa_all gtlabcontainerregistry.azurecr.io/oahpa_all
	podman push gtlabcontainerregistry.azurecr.io/oahpa_all
