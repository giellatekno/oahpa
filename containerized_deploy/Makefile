.PHONY: image run bash shell push-labacr

image:
	podman build -t oahpa_all -f Dockerfile ..

run:
	podman run --rm --name oahpa_all -p 5000:80 oahpa_all

run-bash:
	podman run --rm -it oahpa_all bash

shell:
	podman exec -it oahpa_all bash

push-labacr:
	podman tag oahpa_all gtlabcontainerregistry.azurecr.io/oahpa_all
	podman push gtlabcontainerregistry.azurecr.io/oahpa_all
