from helper import Command, exec_command
import concurrent.futures
import rumps
import time
import re


class AppleMusicController(rumps.App):
	def __init__(self):
		super(AppleMusicController, self).__init__(name="Music")
		self.icon = "AppIcon.icns"
		self.menu = []
		self.CONTROLS = ['Play/Pause','Next','Previous','Stop']
		self.PLAYLIST_COUNT = int(exec_command(Command.GET_PLAYLIST_COUNT))
		self.PLAYLISTS = [rumps.MenuItem(exec_command(Command.GET_PLAYLIST_NAME_BY_ID, n), callback=self.startPlaylist)
					for n in range(1, self.PLAYLIST_COUNT)]
		self.menu = self.CONTROLS+[None]+self.PLAYLISTS+[None]+['Search', 'Sync']+[None]

	def startPlaylist(self, sender):
		exec_command(Command.START_PLAYLIST, sender.title.strip())
		self.playing = True

	def playTrackById(self, trackID):
		exec_command(Command.PLAY_TRACK_BY_ID, trackID)
		self.playing = True

	@rumps.clicked('Play/Pause')
	def playPause(self, sender):
		exec_command(Command.PLAYPAUSE, Command.GET_CURRENT_PLAYLIST_NAME)

	@rumps.clicked('Next')
	def nextTrack(self, sender):
		exec_command(Command.PLAY_NEXT_TRACK)
		self.playing = True

	@rumps.clicked('Previous')
	def previousTrack(self, sender):
		exec_command(Command.PLAY_PREVIOUS_TRACK)
		self.playing = True

	@rumps.clicked('Stop')
	def stopTrack(self, sender):
		exec_command(Command.STOP_TRACK)
		exec_command(Command.QUIT)
		self.menu['Play/Pause'].set_callback(None)
		self.title = None
		self.playing = False

	@rumps.timer(1)
	def updateTitle(self, sender):
		if self.playing:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				executor.submit(self.getPosition)

	def getPosition(self):
		pos = exec_command(Command.GET_TRACK_POSITION)

		if pos!='missing value':
			pos = time.strftime("%M:%S", time.gmtime(float(pos)))

			self.menu['Play/Pause'].set_callback(self.playPause)
			self.title = f"{exec_command(Command.GET_CURRENT_TRACK_NAME)} • {pos}"

		else:
			self.playing = False

	@rumps.clicked('Search')
	def searchAndPlay(self, sender):
		FOUND = False
		window = rumps.Window(f"Search music", ok=None)
		window.icon = self.icon
		response = window.run()

		for playlist in range(1, self.PLAYLIST_COUNT):

			output = exec_command(Command.SEARCH_IN_PLAYLIST, playlist, response.text)
			results = re.findall('\d{3}', output)

			if len(results)>0:
				trackID = results[0]
				track = exec_command(Command.GET_TRACK_NAME_BY_ID, trackID)
				FOUND = True
				break

		if not FOUND:
			self.title = "Nothing to show"
		else:
			self.playTrackById(trackID)

if __name__ == '__main__':
	AppleMusicController().run()







