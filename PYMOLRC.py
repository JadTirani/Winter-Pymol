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
    cmd.deselect()
    return True

# cmd.set("cartoon_oval_length",1)

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


def color_h(selection='all'):
    s = str(selection)
    print(s)
    cmd.set_color('color_ile',[0.996,0.062,0.062])
    cmd.set_color('color_phe',[0.996,0.109,0.109])
    cmd.set_color('color_val',[0.992,0.156,0.156])
    cmd.set_color('color_leu',[0.992,0.207,0.207])
    cmd.set_color('color_trp',[0.992,0.254,0.254])
    cmd.set_color('color_met',[0.988,0.301,0.301])
    cmd.set_color('color_ala',[0.988,0.348,0.348])
    cmd.set_color('color_gly',[0.984,0.394,0.394])
    cmd.set_color('color_cys',[0.984,0.445,0.445])
    cmd.set_color('color_tyr',[0.984,0.492,0.492])
    cmd.set_color('color_pro',[0.980,0.539,0.539])
    cmd.set_color('color_thr',[0.980,0.586,0.586])
    cmd.set_color('color_ser',[0.980,0.637,0.637])
    cmd.set_color('color_his',[0.977,0.684,0.684])
    cmd.set_color('color_glu',[0.977,0.730,0.730])
    cmd.set_color('color_asn',[0.973,0.777,0.777])
    cmd.set_color('color_gln',[0.973,0.824,0.824])
    cmd.set_color('color_asp',[0.973,0.875,0.875])
    cmd.set_color('color_lys',[0.899,0.922,0.922])
    cmd.set_color('color_arg',[0.899,0.969,0.969])
    cmd.color("color_ile","("+s+" and resn ile)")
    cmd.color("color_phe","("+s+" and resn phe)")
    cmd.color("color_val","("+s+" and resn val)")
    cmd.color("color_leu","("+s+" and resn leu)")
    cmd.color("color_trp","("+s+" and resn trp)")
    cmd.color("color_met","("+s+" and resn met)")
    cmd.color("color_ala","("+s+" and resn ala)")
    cmd.color("color_gly","("+s+" and resn gly)")
    cmd.color("color_cys","("+s+" and resn cys)")
    cmd.color("color_tyr","("+s+" and resn tyr)")
    cmd.color("color_pro","("+s+" and resn pro)")
    cmd.color("color_thr","("+s+" and resn thr)")
    cmd.color("color_ser","("+s+" and resn ser)")
    cmd.color("color_his","("+s+" and resn his)")
    cmd.color("color_glu","("+s+" and resn glu)")
    cmd.color("color_asn","("+s+" and resn asn)")
    cmd.color("color_gln","("+s+" and resn gln)")
    cmd.color("color_asp","("+s+" and resn asp)")
    cmd.color("color_lys","("+s+" and resn lys)")
    cmd.color("color_arg","("+s+" and resn arg)")
cmd.extend('color_h',color_h)

def color_h2(selection='all'):
    s = str(selection)
    print(s)
    cmd.set_color("color_ile2",[0.938,1,0.938])
    cmd.set_color("color_phe2",[0.891,1,0.891])
    cmd.set_color("color_val2",[0.844,1,0.844])
    cmd.set_color("color_leu2",[0.793,1,0.793])
    cmd.set_color("color_trp2",[0.746,1,0.746])
    cmd.set_color("color_met2",[0.699,1,0.699])
    cmd.set_color("color_ala2",[0.652,1,0.652])
    cmd.set_color("color_gly2",[0.606,1,0.606])
    cmd.set_color("color_cys2",[0.555,1,0.555])
    cmd.set_color("color_tyr2",[0.508,1,0.508])
    cmd.set_color("color_pro2",[0.461,1,0.461])
    cmd.set_color("color_thr2",[0.414,1,0.414])
    cmd.set_color("color_ser2",[0.363,1,0.363])
    cmd.set_color("color_his2",[0.316,1,0.316])
    cmd.set_color("color_glu2",[0.27,1,0.27])
    cmd.set_color("color_asn2",[0.223,1,0.223])
    cmd.set_color("color_gln2",[0.176,1,0.176])
    cmd.set_color("color_asp2",[0.125,1,0.125])
    cmd.set_color("color_lys2",[0.078,1,0.078])
    cmd.set_color("color_arg2",[0.031,1,0.031])
    cmd.color("color_ile2","("+s+" and resn ile)")
    cmd.color("color_phe2","("+s+" and resn phe)")
    cmd.color("color_val2","("+s+" and resn val)")
    cmd.color("color_leu2","("+s+" and resn leu)")
    cmd.color("color_trp2","("+s+" and resn trp)")
    cmd.color("color_met2","("+s+" and resn met)")
    cmd.color("color_ala2","("+s+" and resn ala)")
    cmd.color("color_gly2","("+s+" and resn gly)")
    cmd.color("color_cys2","("+s+" and resn cys)")
    cmd.color("color_tyr2","("+s+" and resn tyr)")
    cmd.color("color_pro2","("+s+" and resn pro)")
    cmd.color("color_thr2","("+s+" and resn thr)")
    cmd.color("color_ser2","("+s+" and resn ser)")
    cmd.color("color_his2","("+s+" and resn his)")
    cmd.color("color_glu2","("+s+" and resn glu)")
    cmd.color("color_asn2","("+s+" and resn asn)")
    cmd.color("color_gln2","("+s+" and resn gln)")
    cmd.color("color_asp2","("+s+" and resn asp)")
    cmd.color("color_lys2","("+s+" and resn lys)")
    cmd.color("color_arg2","("+s+" and resn arg)")
cmd.extend('color_h2',color_h2)