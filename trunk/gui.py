# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Frame
###########################################################################

class Frame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.Point( 1000,1000 ), size = wx.Size( 300,200 ), style = wx.FRAME_TOOL_WINDOW|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"graphics/arrouw.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		self.button.SetToolTipString( u"Collapse" )
		
		bSizer7.Add( self.button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.movie_load = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.GA_HORIZONTAL|wx.GA_SMOOTH )
		bSizer8.Add( self.movie_load, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.movie_head = wx.HyperlinkCtrl( self, wx.ID_ANY, u"wxFB Website", u"http://www.wxformbuilder.org", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		self.movie_head.SetFont( wx.Font( 13, 70, 90, 90, True, wx.EmptyString ) )
		self.movie_head.SetToolTipString( u"Visit Movie Website" )
		self.movie_head.SetMinSize( wx.Size( 150,25 ) )
		
		bSizer8.Add( self.movie_head, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		bSizer7.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer15.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		self.movie = wx.StaticText( self, wx.ID_ANY, u"Change Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.movie.Wrap( 90 )
		self.movie.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
		self.movie.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		bSizer15.Add( self.movie, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.line = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer15.Add( self.line, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.sub_load = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
		bSizer15.Add( self.sub_load, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.sub = wx.HyperlinkCtrl( self, wx.ID_ANY, u"wxFB Website", u"http://www.wxformbuilder.org", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		self.sub.SetFont( wx.Font( 10, 70, 90, 90, True, wx.EmptyString ) )
		self.sub.SetToolTipString( u"Visit Subtitles Website" )
		
		bSizer9.Add( self.sub, 0, wx.ALL, 5 )
		
		self.sub_apply = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"graphics/play.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 25,25 ), wx.BU_AUTODRAW )
		self.sub_apply.SetToolTipString( u"Play Movie with Subtitles" )
		
		bSizer9.Add( self.sub_apply, 0, 0, 5 )
		
		bSizer15.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer15 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MOTION, self.func )
		self.button.Bind( wx.EVT_BUTTON, self.close )
		self.sub_apply.Bind( wx.EVT_BUTTON, self.sub_restart )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def func( self, event ):
		event.Skip()
	
	def close( self, event ):
		event.Skip()
	
	def sub_restart( self, event ):
		event.Skip()
	

###########################################################################
## Class AboutFrame
###########################################################################

class AboutFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 289,276 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_TOOL_WINDOW|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.dev_label = wx.StaticText( self, wx.ID_ANY, u"\n\nDeveloped by\nVighnesh Birodkar\nemail : vighneshbirodkar@gmail.com\n\nAutoSubtitles Copyright (C) 2012 Vighnesh Birodkar\nThis Program comes with \nABSOLUTELY\nNO WARRANTY\n\nSubtitles thanks to\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.dev_label.Wrap( -1 )
		bSizer10.Add( self.dev_label, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.sub_link = wx.HyperlinkCtrl( self, wx.ID_ANY, u"www.opensubtitles.org", u"www.opensubtitles.org/", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer10.Add( self.sub_link, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.imdb_text = wx.StaticText( self, wx.ID_ANY, u"\nMovie Data Thanks to\nBrian Fritz", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.imdb_text.Wrap( -1 )
		bSizer10.Add( self.imdb_text, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_hyperlink2 = wx.HyperlinkCtrl( self, wx.ID_ANY, u"www.imdbapi.com", u"http://www.imdbapi.com", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		bSizer10.Add( self.m_hyperlink2, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.SetSizer( bSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class SettingsFrame
###########################################################################

class SettingsFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 297,128 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_TOOL_WINDOW|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer11.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Transperency", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText12.Wrap( -1 )
		bSizer16.Add( self.m_staticText12, 1, wx.ALL, 5 )
		
		self.m_slider1 = wx.Slider( self, wx.ID_ANY, 255, 0, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer16.Add( self.m_slider1, 1, wx.ALL, 5 )
		
		bSizer11.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer11 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_slider1.Bind( wx.EVT_SCROLL, self.alpha )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def alpha( self, event ):
		event.Skip()
	

