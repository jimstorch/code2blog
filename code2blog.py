#!/bin/env python

# code2blog, a pyGTK front-end to GNU/Source Highlight
# Copyright (C) 2006 Jim Storch

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import pango
import gobject
import subprocess
import os.path

INPUT_LIST = [
	"bison",
	"c",
	"cpp",
	"caml",
	"changelog",
	"diff",
	"eps",
	"flex",
	"html",
	"java",
	"javascript",
	"latex",
	"logtalk",
	"lua",
	"pascal",
	"perl",
	"postscript",
	"python",
	"ruby",
	"sml",
	"style",
	]

OUTPUT_LIST = [
	"docbook",
	"esc",
	"html",
	"html-css",
	"html-css-doc",
	"html-doc",
	"javadoc",
	"latex",
	"latex-doc",
	"latexcolor",
	"latexcolor-doc",
	"texinfo",
	"xhtml",
	"xhtml-css",
	"xhtml-css-doc",
	"xhtml-doc",
	]

def dependencyCheck():
	try:
		version = subprocess.Popen(
			['source-highlight',"--version"],
			stdout=subprocess.PIPE).communicate()[0]
	except OSError:
		return False  
	else:
		return True

def colorize(text, lang, format, tab_size, line_numbers=False):
	cmd = ["source-highlight",
		"--src-lang", lang,
		"--out-format", format,
		"--tab", tab_size,]

	if line_numbers:
		cmd.append("--line-number-ref")

	child = subprocess.Popen(cmd,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE)
	child.stdin.write(text)
	child.stdin.close()
	html = child.stdout.read()
	return html

	
class MyApp(object):

	def __init__(self):

		# Load our GUI from a glade file
		self.gladefile = "code2blog.glade"  
		self.wTree = gtk.glade.XML(self.gladefile)
		self.window = self.wTree.get_widget("main_window")
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)	

		# Map signals to methods
		dic = { 
			"on_button_open_input_clicked" : self.button_open_input_clicked,
			"on_button_paste_input_clicked" : self.button_paste_input_clicked,
			"on_button_clear_input_clicked": self.button_clear_input_clicked,
			"on_button_apply_clicked" : self.button_apply_clicked,
			"on_button_save_output_clicked" : self.button_save_output_clicked,
			"on_button_copy_output_clicked" : self.button_copy_output_clicked,
			"on_button_clear_output_clicked" : 
				self.button_clear_output_clicked,
			"on_button_about_clicked" : self.button_about_clicked,
			"on_button_quit_clicked" : self.button_quit_clicked,			
			"on_window1_destroy" : gtk.main_quit }
			
		self.wTree.signal_autoconnect(dic)
		
		self.input_view = self.wTree.get_widget("input_view")
		self.input_buffer = self.input_view.get_buffer()
		self.output_view = self.wTree.get_widget("output_view")
		self.output_buffer = self.output_view.get_buffer()

		# Change the TextView font to something monospacey
		self.font_desc = pango.FontDescription('Bitstream Vera Sans Mono')
		self.font_desc.set_size(9000)
		self.input_view.modify_font(self.font_desc)
		self.output_view.modify_font(self.font_desc)

		# populate the input format combo and default to python
		store = gtk.ListStore(gobject.TYPE_STRING)
		for format in INPUT_LIST:
			store.append ([format])
		self.input_format = self.wTree.get_widget("combo_input_format")
		self.input_format.set_model(store)
		cell = gtk.CellRendererText()
		self.input_format.pack_start(cell, True)
		self.input_format.add_attribute(cell, 'text',0)
		self.input_format.set_active(17)

		# populate the output format combo and default to HTML
		store = gtk.ListStore(gobject.TYPE_STRING)
		for format in OUTPUT_LIST:
			store.append ([format])
		self.output_format = self.wTree.get_widget("combo_output_format")
		self.output_format.set_model(store)
		cell = gtk.CellRendererText()
		self.output_format.pack_start(cell, True)
		self.output_format.add_attribute(cell, 'text',0)
		self.output_format.set_active(2)

		# Controls to tab size and whether to show line numbers		
		self.tab_size = self.wTree.get_widget("spinner_tab_size")
		self.check_number = self.wTree.get_widget("check_number")
		self.clipboard = gtk.Clipboard()
		self.last_filename = "new"
		self.last_format = "html"
		
	def button_open_input_clicked(self, widget):
		chooser = gtk.FileChooserDialog(
			title="Open Source File",action=gtk.FILE_CHOOSER_ACTION_OPEN,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		response = chooser.run()

		if response == gtk.RESPONSE_OK:
			filename = chooser.get_filename()
			file_object = open(filename,'r')
			try:
				contents = file_object.read()
			finally:
				file_object.close()
			self.input_buffer.set_text(contents)	

		chooser.destroy()		

	def button_paste_input_clicked(self, widget):
		self.input_buffer.paste_clipboard(
			self.clipboard, None, self.input_view.get_editable())
		
	def button_clear_input_clicked(self, widget):
		self.input_buffer.set_text("")

	def button_apply_clicked(self, widget):
		start, end = self.input_buffer.get_bounds()
		src = self.input_buffer.get_text(start, end)
		tabs = str(int(self.tab_size.get_value()))
		lang = self.input_format.get_active_text()
		format = self.output_format.get_active_text()
		show_line_numbers=self.check_number.get_active()
		output = colorize(src, lang=lang, format=format,
			tab_size=tabs, line_numbers=show_line_numbers)
		self.output_buffer.set_text(output)
		start, end = self.output_buffer.get_bounds()
		self.output_buffer.select_range(start, end)		

	def button_save_output_clicked(self, widget):
		chooser = gtk.FileChooserDialog(
			title="Save Output",action=gtk.FILE_CHOOSER_ACTION_SAVE,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
			gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		response = chooser.run()
	
		if response == gtk.RESPONSE_OK:
			filename = chooser.get_filename()
			file_exists = False
			file_overwrite = False
  	
  			if os.path.isfile(filename):
  				# if the file already exists
				file_exists = True
				warning_message = (
					"Are you sure you want to overwrite:\n" + 
					filename +
					"\nwith the contents of the OUTPUT window?\n\n"
					"Think before you click." ) 
				warning = gtk.MessageDialog(None, gtk.DIALOG_MODAL, 
					gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE, warning_message)
				warning.add_button(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL)
				warning.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
	
				if warning.run() == gtk.RESPONSE_OK:
					# exists, but user said ok to overwrite
					file_overwrite = True
  				warning.destroy()
  	
  			if (file_exists == False) or ( file_exists == True and
				file_overwrite == True ):
				file_object = open(filename,'w')
				start, end = self.output_buffer.get_bounds()
				contents = self.output_buffer.get_text(start, end)
				try:
					file_object.write(contents)
				finally:
					file_object.close()
	
		chooser.destroy()

	def button_copy_output_clicked(self, widget):
		self.output_buffer.copy_clipboard(self.clipboard)

	def button_clear_output_clicked(self, widget):
		self.output_buffer.set_text("")	
		
	def button_about_clicked(self, widget):
		pass

	def button_quit_clicked(self, widget):
		gtk.main_quit()

		
if __name__ == "__main__":
	if dependencyCheck():
		MyApp()
		gtk.main()
	else:
		print ( "Please install GNU/Source Highlight, "
			"http://www.gnu.org/software/src-highlite" )
