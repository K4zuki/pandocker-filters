ifeq ($(OS),Windows_NT)
HOME = C:/Users/$(USERNAME)
endif
PIPBASE= $(shell get-pip-base)
PANSTYLES= $(PIPBASE)/var
MISC= $(PANSTYLES)/pandoc_misc
MISC_SYS = $(MISC)/system
MISC_USER = $(MISC)/user
include $(MISC_SYS)/Makefile.in
PROJECT= `pwd`

## userland: uncomment and replace
# MDDIR:= markdown
# DATADIR:= data
# TARGETDIR:= Out
# IMAGEDIR:= images

# CONFIG:= config.yaml
# INPUT:= TITLE.md
# TARGET:= TARGET-$(DATE)-$(HASH)
# REFERENCE:= $(MISC)/ref.docx
# COREPROPFLAGS := --table "Normal Table=Centered"
# COREPROPFLAGS += --paragraph "Normal=Body Text"
##

PANFLAGS =
PANFLAGS += $(MISC_SYS)/$(CONFIG)
PANFLAGS += $(MDDIR)/$(CONFIG)

#PANFLAGS += --filter=../pandoc_pandocker_filters/bitfield_inline.py
#PANFLAGS += --filter=../pandoc_pandocker_filters/BitField.py
PANFLAGS += --filter=../pandoc_pandocker_filters/ListingTable.py
PANFLAGS += --filter=../pandoc_pandocker_filters/listingtable_inline.py
PANFLAGS += --filter=../pandoc_pandocker_filters/wavedrom_inline.py
#PANFLAGS += --filter=../pandoc_pandocker_filters/RotateImage.py
PANFLAGS += --filter=../pandoc_pandocker_filters/rotateimage_inline.py
PANFLAGS += --filter=../pandoc_pandocker_filters/AAFigure.py
PANFLAGS += --filter=../pandoc_pandocker_filters/aafigure_inline.py
PANFLAGS += --filter=../pandoc_pandocker_filters/pantable_inline.py

PANFLAGS += --filter=pandoc-crossref
include $(MISC_SYS)/Makefile
