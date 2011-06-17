from plotstuff_c import *

# Could consider using swig's "addmethods" mechanism to create this "class" rep.

class Plotstuff(object):
	format_map = {'png': PLOTSTUFF_FORMAT_PNG,
				  'jpg': PLOTSTUFF_FORMAT_JPG,
				  'ppm': PLOTSTUFF_FORMAT_PPM,
				  'pdf': PLOTSTUFF_FORMAT_PDF,
				  'fits': PLOTSTUFF_FORMAT_FITS,
				  }
				  

	def __init__(self, outformat=None, size=None, ra=None, dec=None, width=None,
				 rdw=None, wcsfn=None, wcsext=0):
		p = plotstuff_new()
		self.pargs = p
		if outformat is not None:
			outformat = Plotstuff.format_map.get(outformat, outformat)
			self.outformat = outformat
		if size is not None:
			self.size = size
			self.color = 'black'
			self.plot('fill')
		if ra is not None and dec is not None and width is not None:
			self.set_wcs_box(ra, dec, width)
		if rdw is not None:
			self.set_wcs_box(*rdw)
		if wcsfn is not None:
			self.wcs_file = (wcsfn, wcsext)
			if size is None:
				plotstuff_set_size_wcs(self.pargs)

	def __del__(self):
		#print 'plotstuff.__del__, pargs=', self.pargs
		plotstuff_free(self.pargs)

	def __getattr__(self, name):
		if name == 'xy':
			return plot_xy_get(self.pargs)
		elif name == 'index':
			return plot_index_get(self.pargs)
		elif name == 'radec':
			return plot_radec_get(self.pargs)
		elif name == 'match':
			return plot_match_get(self.pargs)
		elif name == 'image':
			return plot_image_get(self.pargs)
		elif name == 'outline':
			return plot_outline_get(self.pargs)
		elif name == 'grid':
			return plot_grid_get(self.pargs)
		elif name in ['ann', 'annotations']:
			return plot_annotations_get(self.pargs)
		elif name == 'healpix':
			return plot_healpix_get(self.pargs)
		return self.pargs.__getattr__(name)

	def __setattr__(self, name, val):
		if name == 'pargs':
			#print 'plotstuff.py: setting pargs to', val
			self.__dict__[name] = val
		elif name == 'size':
			#print 'plotstuff.py: setting plot size of', self.pargs, 'to %i,%i' % (val[0], val[1])
			plotstuff_set_size(self.pargs, val[0], val[1])
		elif name == 'color':
			#print 'plotstuff.py: setting color to "%s"' % val
			self.set_color(val)
		elif name == 'rgb':
			plotstuff_set_rgba2(self.pargs, val[0], val[1], val[2],
						   plotstuff_get_alpha(self.pargs))
		elif name == 'alpha':
			self.set_alpha(val)
		elif name == 'lw':
			self.pargs.lw = float(val)
		elif name == 'marker' and type(val) is str:
			plotstuff_set_marker(self.pargs, val)
		elif name == 'markersize':
			plotstuff_set_markersize(self.pargs, val)
		elif name == 'wcs_file':
			if type(val) is tuple:
				plotstuff_set_wcs_file(self.pargs, *val)
			else:
				plotstuff_set_wcs_file(self.pargs, val, 0)
		elif name == 'wcs':
			plotstuff_set_wcs(self.pargs, val)
		elif name == 'text_bg_alpha':
			plotstuff_set_text_bg_alpha(self.pargs, val)
		#elif name == 'operator':
		#	print 'val:', val
		#	self.pargs.op = val
		else:
			self.pargs.__setattr__(name, val)

	def get_image_as_numpy(self):
		return self.pargs.get_image_as_numpy()

	def apply_settings(self):
		plotstuff_builtin_apply(self.pargs.cairo, self.pargs)

	def plot(self, layer):
		return plotstuff_plot_layer(self.pargs, layer)

	def scale_wcs(self, scale):
		plotstuff_scale_wcs(self.pargs, scale)

	def rotate_wcs(self, angle):
		plotstuff_rotate_wcs(self.pargs, angle)

	def set_wcs_box(self, ra, dec, width):
		plotstuff_set_wcs_box(self.pargs, ra, dec, width)

	def set_color(self, color):
		#print 'calling plotstuff_set_color(., \"%s\")' % color
		x = plotstuff_set_color(self.pargs, color)
		return x

	def set_alpha(self, a):
		x = plotstuff_set_alpha(self.pargs, a)

	def plot_grid(self, rastep, decstep, ralabelstep=None, declabelstep=None):
		grid = plot_grid_get(self.pargs)
		grid.rastep = rastep
		grid.decstep = decstep
		if ralabelstep is None:
			ralabelstep = 0
		if declabelstep is None:
			declabelstep = 0
		grid.ralabelstep = ralabelstep
		grid.declabelstep = declabelstep
		self.plot('grid')
		
	def write(self, filename=None):
		if filename is not None:
			self.outfn = filename
		plotstuff_output(self.pargs)

	def text_xy(self, x, y, text):
		plotstuff_text_xy(self.pargs, x, y, text)

	def text_radec(self, ra, dec, text):
		plotstuff_text_radec(self.pargs, ra, dec, text)

	def stack_marker(self, x, y):
		plotstuff_stack_marker(self.pargs, x, y)

	def set_markersize(self, size):
		plotstuff_set_markersize(self.pargs, size)

	def plot_stack(self):
		plotstuff_plot_stack(self.pargs, self.pargs.cairo)

