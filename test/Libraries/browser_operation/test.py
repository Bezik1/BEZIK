import mechanize

br = mechanize.Browser()

br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; es-VE;  rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]

r = br.open("http://www.google.com/")
print(br.forms())

br.select_form(nr=0)
br["q"] = "siema"
br.submit()