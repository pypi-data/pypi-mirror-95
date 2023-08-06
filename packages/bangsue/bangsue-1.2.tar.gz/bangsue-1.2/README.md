![Bangsue_Image](https://github.com/aphisitworachorch/bangsue/blob/master/bangsue.jpg)

# Bangsue
Thai Codename Generator (Data from data.go.th)

## Installation

    pip install bangsue
 ---
 ##  Example Code
 
    from bangsue_codename import BangsueCodename
    bangsue_get = BangsueCodename.Bangsue()
    codename = bangsue_get.get_code_name()
    print(bangsue_get.convert_codename_to_string(codename,"all"))
    
    RESULT : huapluak_saohai_saraburi