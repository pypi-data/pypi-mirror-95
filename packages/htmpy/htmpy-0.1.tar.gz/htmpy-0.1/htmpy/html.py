

class tag:
	"""tag element"""
	def __init__(self,_type,attributes={}):
		"""generate a tag element
		attributes correspond to the html attributes
		_type corresponds to the tag name"""
		self.attributes = attributes
		self.type = _type
		self.children = []

	def generate_attributes(self):
		"""generate a string with all the attributes
		like this : attrname = \"value\""""
		r = ' '

		if self.attributes == {}:
			return ''

		for attn,value in self.attributes.items():
			r+= attn + " = \"" + value + "\" "


		return r

	def render(self,d=0):
		"""generate the tag as a string with chidrens and text inside"""
		r = ''
		r+='<'+self.type
		r+=self.generate_attributes()
		r+='>\n'
		for c in self.children:
			r+='\t'*(d+1)
			if type(c) == tag:
				r+=c.render(d=d+1)
			else:
				r+=str(c)
			r+='\n'
		r+='\t'*d
		r+='</'+self.type+'>'
		return r

	def add(self,toadd):
		"""add a new children. It can be a tag or text"""
		self.children.append(toadd)

if __name__ == '__main__':
	attributes = {}
	attributes['lang'] = 'fr'
	root = tag('html',attributes=attributes)
	body = tag('body')
	p1 = tag('p')

	root.add(body)
	p1.add('test')
	body.add(p1)

	print(root.render())