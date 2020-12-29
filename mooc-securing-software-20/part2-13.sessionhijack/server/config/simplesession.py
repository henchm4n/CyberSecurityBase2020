import django.contrib.sessions.backends.db as db

class SessionStore(db.SessionStore):
	session_counter = 0

	def _get_new_session_key(self):
		while True:
			session_key = 'session-' + str(SessionStore.session_counter)
			SessionStore.session_counter += 1
			if not self.exists(session_key):
				return session_key
