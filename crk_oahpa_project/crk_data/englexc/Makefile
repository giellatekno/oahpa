# ****************************************************************** #
# This is a makefile that builds the training morphological parser 7 #
# ****************************************************************** #

XFST = xfst #-utf8
LEXC = lexc #-utf8
TWOLC = twolc #-utf8

ieng.fst: engraw.fst eng.fst inituppercase.fst
	@echo
	@echo "*** Building the inverse eng.fst ***" ;
	@echo
	printf "load engraw.fst \n\
	invert net \n\
	save stack ieng.fst \n\
	quit \n" > if-fst-script
	$(XFST) < if-fst-script
	rm -f if-fst-script


eng.fst: engraw.fst inituppercase.fst
	@echo
	@echo "*** Building the eng.fst ***" ;
	@echo
	@printf "read regex @\"engraw.fst\" .o. \
	@\"inituppercase.fst\" ; \n\
	save stack eng.fst \n\
	quit \n " > eng-case-fst-script
	$(XFST) < eng-case-fst-script
	@rm -f eng-case-fst-script


engraw.fst: eng.lexc eng.bin
	@echo
	@echo "*** Building engraw.fst ***" ;
	@echo
	printf "compile-source eng.lexc \n\
	read-rules eng.bin \n\
	compose-result \n\
	save-result engraw.fst \n\
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

inituppercase.fst: inituppercase.regex 
	@echo
	@echo "*** Building inituppercase.fst ***" ;
	@echo
	@printf "read regex < inituppercase.regex \n\
	save stack inituppercase.fst \n\
	quit \n" > inituppercase-script
	$(XFST) < inituppercase-script
	@rm -f inituppercase-script




clean:
	@rm -f eng.bin eng.fst ieng.fst engraw.fst inituppercase.fst



