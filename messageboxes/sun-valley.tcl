# Copyright © 2021 rdbende <rdbende@gmail.com>

source [file join [file dirname [info script]] theme light.tcl]
source [file join [file dirname [info script]] theme dark.tcl]

option add *tearOff 0

proc set_theme {mode} {
	if {$mode == "dark"} {
		ttk::style theme use "sun-valley-dark"

        namespace eval themeColors {
            set fg             "#ffffff"
            set bg             "#1c1c1c"
            set disabledFg     "#595959"
            set selectFg       "#ffffff"
            set selectBg       "#2f60d8"
            set dialogInfoBg   "#2b2b2b"
            set menuBg         "#2f2f2f"
            set treeSelectBg   "#292929"
        }
        
        ttk::style configure . \
            -background $themeColors::bg \
            -foreground $themeColors::fg \
            -troughcolor $themeColors::bg \
            -focuscolor $themeColors::selectBg \
            -selectbackground $themeColors::selectBg \
            -selectforeground $themeColors::selectFg \
            -insertwidth 1 \
            -insertcolor $themeColors::fg \
            -fieldbackground $themeColors::bg \
            -font {"Segoe UI" 10} \
            -borderwidth 0 \
            -relief flat

        tk_setPalette \
        	background [ttk::style lookup . -background] \
            foreground [ttk::style lookup . -foreground] \
            highlightColor [ttk::style lookup . -focuscolor] \
            selectBackground [ttk::style lookup . -selectbackground] \
            selectForeground [ttk::style lookup . -selectforeground] \
            activeBackground [ttk::style lookup . -selectbackground] \
            activeForeground [ttk::style lookup . -selectforeground]
        
        ttk::style map . -foreground [list disabled $themeColors::disabledFg]

        option add *font [ttk::style lookup . -font]
        option add *Menu.selectcolor $themeColors::fg
        option add *Menu.background $themeColors::menuBg
    
	} elseif {$mode == "light"} {
		ttk::style theme use "sun-valley-light"

        namespace eval themeColors {
            set fg             "#202020"
            set bg             "#fafafa"
            set disabledFg     "#a0a0a0"
            set selectFg       "#ffffff"
            set selectBg       "#2f60d8"
            set dialogInfoBg   "#ffffff"
            set menuBg         "#e7e7e7"
            set treeSelectFg   "#191919"
            set treeSelectBg   "#f0f0f0"
        }

        ttk::style configure . \
            -background $themeColors::bg \
            -foreground $themeColors::fg \
            -troughcolor $themeColors::bg \
            -focuscolor $themeColors::selectBg \
            -selectbackground $themeColors::selectBg \
            -selectforeground $themeColors::selectFg \
            -insertwidth 1 \
            -insertcolor $themeColors::fg \
            -fieldbackground $themeColors::bg \
            -font {"Segoe UI" 10} \
            -borderwidth 0 \
            -relief flat

        tk_setPalette \
            background [ttk::style lookup . -background] \
            foreground [ttk::style lookup . -foreground] \
            highlightColor [ttk::style lookup . -focuscolor] \
            selectBackground [ttk::style lookup . -selectbackground] \
            selectForeground [ttk::style lookup . -selectforeground] \
            activeBackground [ttk::style lookup . -selectbackground] \
            activeForeground [ttk::style lookup . -selectforeground]
        
        ttk::style map . -foreground [list disabled $themeColors::disabledFg]

        option add *font [ttk::style lookup . -font]
        option add *Menu.selectcolor $themeColors::fg
        option add *Menu.background $themeColors::menuBg
	}
}
