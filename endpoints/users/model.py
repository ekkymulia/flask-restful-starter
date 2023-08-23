from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),
                        nullable=False, default=2)

    def __repr__(self):
        return 'Id: {}, username: {}, password: {}, role_id: {}'.format(self.id, self.username, self.password, self.role_id)