from ebookdio import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(256))
    author = db.Column(db.Unicode(256))

    @property
    def short_title(self):
        max_len = 30
        if len(self.title) > max_len:
            return self.title[:max_len] + '...'
        else:
            return self.title
