"""
example from status.config

resolution {
	output = 'eDP1'
	options = [ '3200x1800', '1920x1080' ]
	format = '[ {output}: {resolution} ]'
	commandAfter = 'feh --bg-scale ~/wallpaper.jpg'
}

"""
import subprocess
import os 

class Py3status:
    output = 'non'
    options = []

    def _getResolution(self):
        res = subprocess.check_output("xrandr | grep {output} | egrep -o '([0-9]+x[0-9]+)'".format(output=self.output), shell=True)
        self.currentResolution = res.decode().replace('\n','')
    
    def _setNextResolution(self):
        i = 0
        while( i < len(self.options) ):
            i = (i + 1) % len(self.options)
            yield self.options[i]
        while( True ):
            yield 'non'

    def __init__(self):
        self.gen = self._setNextResolution()

    def resolution(self):
        self._getResolution()
        format = self.format.format(output = self.output, resolution = self.currentResolution)
        return {
            'full_text' : format,
            'cached_until': self.py3.CACHE_FOREVER
        }

    def on_click(self, event):
        self.currentResolution = next(self.gen)
        baseCmd = 'xrandr --output {output} --mode {option}'
        command = baseCmd.format(output = self.output, option = self.currentResolution)
        os.system(command)
        os.system(self.commandAfter)
