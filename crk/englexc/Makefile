# ****************************************************************** #
# This is a makefile that builds the training morphological parser 7 #
# ****************************************************************** #

XFST = xfst #-utf8
LEXC = lexc #-utf8
TWOLC = twolc #-utf8

ieng.fst: eng.fst
	@echo
	@echo "*** Building the inverse eng.fst ***" ;
	@echo
	printf "load eng.fst \n\
	invert net \n\
	save stack ieng.fst \n\
	quit \n" > if-fst-script
	$(XFST) < if-fst-script
	rm -f if-fst-script


eng.fst: eng.lexc eng.bin
	@echo
	@echo "*** Building eng.fst ***" ;
	@echo
	printf "compile-source eng.lexc \n\
	read-rules eng.bin \n\
	compose-result \n\
	save-result eng.fst \n\
	quit \n" > f-fst-script
	$(LEXC) < f-fst-script
	rm -f f-fst-script

eng.bin: eng.twolc
	@echo
	@echo "*** Building eng.bin ***" ;
	@echo
	@printf "read-grammar eng.twolc \n\
	compile \n\
	save-binary eng.bin \n\
	quit \n" > f-bin-script
	$(TWOLC) < f-bin-script
	@rm -f f-bin-script

clean:
	@rm -f eng.bin eng.fst ieng.fst


