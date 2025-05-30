import string
from enum import Enum
from pymol import cmd, util

"""
Winter's PYMOLRC
This file contains a collection of functions to help with PYMOL scripting.
"""

@cmd.extend
def ASSERT(passthru_msg = "") :
    """
    Allows for debugging inside of the Winter suite of function
    """
    print(f"Winter>{passthru_msg}")

# Cleans up the protien picture
def STRIP_CLEAN(Tag="all") -> bool:
    cmd.select(Tag)
    cmd.remove("solvent")
    cmd.set("sphere_scale", 0.55)
    cmd.set("cartoon_oval_length",1)
    cmd.deselect()
    return True


# Strips all ions and peripheral molecules
def ION_STRIP() :
    cmd.remove("resn SO4")
    cmd.remove("resn GOL")
    cmd.remove("resn EDO")

# A combination of all stripping functions
def SUPER_STRIP() :
    STRIP_CLEAN()
    ION_STRIP()

# Regular align but makes it so that your starting object is the parent for alignment. The child moves TO the parent.
def ALIGN_FROM(passthru_parent, passthru_child) :
    cmd.align(passthru_child, passthru_parent)

def SUPER_FROM(passthru_parent, passthru_child) :
    cmd.super(passthru_child,passthru_parent)

# Enter codes as "PDBentry,newname" and it will automatically rename all the objects
def FETCH(*passthru_multi) :
    for single in passthru_multi :
        PDBentry, PYMOLname = single.split(',')
        cmd.fetch(PDBentry)
        cmd.set_name(PDBentry, PYMOLname)

# Removes the object with exception to the kept selection
def REMOVE_EXCEPT(passthru_obj, passthru_exception) :
    cmd.remove(passthru_obj + " and not " + passthru_exception)

# Displays main and side chains along with revealing polar contacts within the selction
def REVEAL(passthru_sel) :
    cmd.show("sticks", f"{passthru_sel} and backbone")
    cmd.show("sticks", f"{passthru_sel} and not backbone")

# Selects all residues within 5 angstroms of the object. You can use passthru_valid to choose objects or selections included in the search
def SELECT_5A(passthru_sel, passthru_parent, passout_name = "temp",mode = "byres") :
    cmd.select(passout_name, mode + " " + passthru_parent + " within 5 of " + passthru_sel)

def PC(passthru_sel, passout_name = "temp") :
    cmd.dist(passout_name,f"({passthru_sel}) and not (solvent)",f"({passthru_sel}) and not (solvent)",quiet=1,mode=2,label=0,reset=1)
    cmd.enable(passout_name)
    cmd.color("orange",passout_name)

def PC_5A(passthru_sel, passthru_parent):
    A5_SEL = "5A_"+passthru_parent
    PC5A_OBJ = "PC5A_"+passthru_parent

    SELECT_5A(passthru_sel, passthru_parent, A5_SEL)
    cmd.color("forest",A5_SEL)
    cmd.color("yellow", passthru_sel)
    util.cnc(passthru_sel,_self=cmd)
    REVEAL(A5_SEL)

    cmd.dist(PC5A_OBJ,f"({A5_SEL}) and not (solvent)",f"({A5_SEL}) and not (solvent)",quiet=1,mode=2,label=0,reset=1)
    cmd.enable(PC5A_OBJ)
    cmd.color("orange",PC5A_OBJ)

# Sets background colour
def COLOUR_BG(passthru_colour) : 
    cmd.bg_color(passthru_colour)

def LABEL_STYLE(passthru_sel="", text_colour = "black", bkg_colour = "white", transparency="0.4"):
    cmd.set("label_color", text_colour, '?_labeledit02', quiet=0)
    cmd.set("label_bg_color", bkg_colour, '?_labeledit02', quiet=0)
    cmd.get_wizard().set_bg_transparency(transparency)

# Colours an object by secondary structures
def COLOUR_BY_SS(passthru_obj="all", body_colour = "deepteal", alpha_colour = "red", beta_colour="purpleblue"):
    cmd.color(body_colour, passthru_obj)
    cmd.color(alpha_colour, passthru_obj + " and ss l+")
    cmd.color(beta_colour, passthru_obj + " and ss s")
    cmd.set("cartoon_discrete_colors", 1)

def COLOUR_LIGAND(passthru_ligand) :
    cmd.color()

def LABEL_SELECTION(passthru_exp, passthru_sele="(sele)", passthru_labelsize = 1) :
    cmd.label(passthru_sele, passthru_exp)
    cmd.set("label_background","white")
    cmd.set("label_color","black")
    cmd.set("label_size", passthru_labelsize)
