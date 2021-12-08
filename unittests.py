import os
import unittest
from flask import Flask
from app.views import country
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        db.session.add(models.Country(name='Poland',capital='Warsaw',lat="52.23",lang="21.01",language='Polish', currency='PLN'))
        db.session.add(models.Country(name='Germany',capital='Berlin',lat="52.23",lang="21.01",language='German', currency='EUR'))
        db.session.add(models.Country(name='France',capital='Paris',lat="52.23",lang="21.01",language='French', currency='EUR'))

        db.session.add(models.User(name='John',username="johnny123" ,password='123', email="john@email.com", isAdmin=True ))
        db.session.add(models.User(name='Paul',username="paul123" ,password='123', email="paul@email.com", isAdmin=False ))
        db.session.add(models.User(name='George',username="george123" ,password='123', email="george@email.com", isAdmin=False ))

        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test user admin
    def test_user_admin(self):
        user = models.User.query.filter_by(username="johnny123").first()
        user2 = models.User.query.filter_by(username="george123").first()
        self.assertTrue(user.isAdmin)
        self.assertFalse(user2.isAdmin)

    # Test databese queries
    def test_country_query_name(self):
        country = models.Country.query.filter_by(name='Poland').first()
        self.assertEqual(country.name, 'Poland')
        self.assertEqual(country.capital, 'Warsaw')
        self.assertEqual(country.lat, "52.23")
        self.assertEqual(country.lang, "21.01")
        self.assertEqual(country.language, 'Polish')
        self.assertEqual(country.currency, 'PLN')

    def test_user_query_capital(self):
        country = models.Country.query.filter_by(capital='Warsaw').first()
        self.assertEqual(country.name, 'Poland')
        self.assertEqual(country.capital, 'Warsaw')
        self.assertEqual(country.lat, "52.23")
        self.assertEqual(country.lang, "21.01")
        self.assertEqual(country.language, 'Polish')
        self.assertEqual(country.currency, 'PLN')

    def test_user_query_username(self):
        user = models.User.query.filter_by(username="johnny123").first()
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.username, 'johnny123')
        self.assertEqual(user.password, '123')
        self.assertEqual(user.email, 'john@email.com')
    
    def test_user_query_email(self):
        user = models.User.query.filter_by(email="paul@email.com").first()
        self.assertEqual(user.name, 'Paul')
        self.assertEqual(user.username, 'paul123')
        self.assertEqual(user.password, '123')
        self.assertEqual(user.email, 'paul@email.com')

    # test sorting query
    def test_sort_query(self):
        countrylist = models.Country.query.order_by(models.Country.name).all()
        self.assertEqual(countrylist[0].name, 'France')
        self.assertEqual(countrylist[1].name, 'Germany')
        self.assertEqual(countrylist[2].name, 'Poland')

    # test relations between the tables
    def test_user_country(self):
        user = models.User.query.filter_by(username="johnny123").first()
        user1 = models.User.query.filter_by(username="paul123").first()
        user2 = models.User.query.filter_by(username="george123").first()

        country = models.Country.query.filter_by(name='Poland').first()
        country.citizens.append(user)
        country.citizens.append(user1)
        country.visitors.append(user2)
        country.visitors.append(user)
        country.futureVisitors.append(user2)
        country.futureVisitors.append(user1)
        self.assertEqual(country.citizens[0], user)
        self.assertEqual(country.citizens[1], user1)
        self.assertEqual(country.visitors[0], user2)
        self.assertEqual(country.visitors[1], user)
        self.assertEqual(country.futureVisitors[0], user2)
        self.assertEqual(country.futureVisitors[1], user1)

    def test_country_user(self):
        user = models.User.query.filter_by(username="johnny123").first()
        country = models.Country.query.filter_by(name='Poland').first()
        country2 = models.Country.query.filter_by(name='Germany').first()
        country3 = models.Country.query.filter_by(name='France').first()
        user.bucketList.append(country)
        user.bucketList.append(country2)
        user.visitedCountries.append(country3)
        user.visitedCountries.append(country2)
        self.assertEqual(user.bucketList[0], country)
        self.assertEqual(user.bucketList[1], country2)
        self.assertEqual(user.visitedCountries[0], country3)
        self.assertEqual(user.visitedCountries[1], country2)

    # Test routes
    def test_indexroute(self):
        response = self.app.get('/',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_loginroute(self):
        response = self.app.get('/login',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_registerroute(self):
        response = self.app.get('/register',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_countryroute(self):
        response = self.app.get('/country/Poland',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profileroute(self):
        response = self.app.get('/profile/johnny123',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_accountroute(self):
        response = self.app.get('/account',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_respondroute(self):
        response = self.app.get('/respond',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 405)

    def test_ctryrmvroute(self):
        response = self.app.get('/ctryrmv',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 405)

    def test_adminroute1(self):
        response = self.app.get('/admin',
                               follow_redirects=True)
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()

        