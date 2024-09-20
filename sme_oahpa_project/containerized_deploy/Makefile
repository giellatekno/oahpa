.PHONY: help run run-bash image shell push-labacr

help:
	@echo "Available commands:"
	@echo "image: build container image"
	@echo "run: run built container image"
	@echo "run-bash: run build container image, but run bash instead of app"
	@echo "shell: exec bash in the running container"

image:
	podman build -f Dockerfile -t oahpa_sme ..

run:
	podman run --rm -it --name oahpa_sme -p 5050:80 oahpa_sme

run-bash:
	podman run --rm -it --name oahpa_sme -p 5050:80 oahpa_sme bash

shell:
	podman exec -it oahpa_sme bash

push-labacr:
	podman tag oahpa_sme gtlabcontainerregistry.azurecr.io/oahpa_sme
	podman push gtlabcontainerregistry.azurecr.io/oahpa_sme
