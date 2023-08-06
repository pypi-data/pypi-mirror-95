miat-Manual Image Analysis Tools

This library's purpose is to help measuring graphics and figures directly in your python IDLE instead of having to save them, then use programs like ImageJ to measure parameters. 

If you want to use this, just pip install miat.

From there, importing miat.tools will allow you to use miat's tools. There aren't many for now, but I'll eventually add more. The tools currently in place will allow you to add horizontal and vertcal bars to a figure or image, which is useful for measuring deltas, for example. The second tool allows you to add circular markers to a figure. One usecase I can think of would be to measure circular diffraction patterns.

All markers can be used in groups of 1, 2 or 3, which will have the same color. The lines can span across multiple axes, or specific axes if you provide the optional axes list parameter. This library also works for imshow figures.


I have added some documentation [here](https://github.com/CephalonAhmes/miat/tree/main/documentation)