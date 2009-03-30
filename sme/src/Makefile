# ******************************************************************** #
# Makefile for pedacogical tools
# ******************************************************************** #
# Version $Id: $


# =============================== #
# Variable definitions          #
# =============================== #

VISLCG3 = /opt/smi/common/bin/vislcg3
TARGET = sme
RULES = ped.cg3
OPTDIR = /opt/smi/$(TARGET)/bin/

dis-bin: ../bin/$(TARGET)-$(RULES).bin
../bin/$(TARGET)-$(RULES).bin: $(TARGET)-$(RULES)
	@echo
	@echo "*** Building $(TARGET)-$(RULES).bin ***"
	@echo "Note: This requires a relatively new vislcg3 file."
	@echo "The morphological parsers are not affected if you"
	@echo "fail to build this file, it is for disambiguation."
	@echo
	@echo
	mkdir -p ../bin
	$(VISLCG3) -g $(TARGET)-$(RULES) --grammar-only --grammar-bin ../bin/$(TARGET)-$(RULES).bin

copy-dis: dis-bin
copy-dis:
	@echo
	@echo "Copying ped-rules to $(OPTDIR)"
	@echo "requires sudo-rights"
	@echo
	sudo cp ../bin/$(TARGET)-$(RULES).bin $(OPTDIR)
