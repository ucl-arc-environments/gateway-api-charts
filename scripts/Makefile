.PHONY: *

GATEWAY_API_VERSION = "v1.4.1"

define fetch_crds
	python crds.py -c $(1) -v $(GATEWAY_API_VERSION)
endef

experimental:
	$(call fetch_crds,experimental)

standard:
	$(call fetch_crds,standard)

all:
	$(call fetch_crds,experimental)
	$(call fetch_crds,standard)
