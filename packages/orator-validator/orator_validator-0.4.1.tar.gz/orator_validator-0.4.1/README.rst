Orator Validator
################

|Downloads|

.. |Downloads| image:: https://pepy.tech/badge/orator-validator
   :target: https://pepy.tech/project/orator-validator

This is a orator plugin that you can use to validate
your model when the user is creating a new item or
updating one on the database is easy to use and cleans
the code a lot

Installation
============

You can install the plugin by using pip

.. code-block:: bash

  $ pip install orator-validator


How to use it
=============

Setup
-----

this is an example of how to implement on your orator model


.. code-block:: python

  from orator import Model
  from orator_validator import Validator


  class User(Model, Validator):

      __connection__ = 'local'
      __fillable__ = [
            'name', 'email', 'password', 'phone_number'
      ]
      __guarded__ = ['id', 'password']


  class UserValidation(object):
    '''Here goes the validations that you need'''

  User.observe(UserValidation())

Functions available
-------------------

Validate saving function
~~~~~~~~~~~~~~~~~~~~~~~~

the validate function accepts this params

* **require:** boolean when True checks if they send the value
* **data_type:** object Verifies if the value is specific data type
* **regex:** string pass a regex to verified
* **date_str:** string witch you want to check the format of the date example '%H:%M'

Example
~~~~~~~

.. code-block:: python

  def saving(self, user):
      user.validate('name', require=True, data_type=str)
      user.validate(
          'email', regex="(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
      )
      user.validate(
          'password', regex="^(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{6,}$"
      )
      user.errors()

Validate update function
~~~~~~~~~~~~~~~~~~~~~~~~

the validate_update accepts this params

* **guarded:** boolean if True value cannot be updated
* **data_tpe:** needs to send specific data type
* **regex:** regex to validate the value
* **date_str:** string to validate a date format
* **function_callback:** callback function if the value was send
* **args:** arguments for the function callbacks

Example
~~~~~~~

.. code-block:: python

  def updating(self, user):
      user.validate_update('email', guarded=True)
      user.validate_update(
        'password', function_callback=self.__validate_new_password, user=user
      )
      user.errors()

  def __validate_new_password(self, user):
      '''
      Validate that the new password is diferent than the old one
      '''
      User.find(user.id)
      if user.password == User.find(user.id).password:
        raise Exception("Can't update password with old one")

Process function
~~~~~~~~~~~~~~~~

the process function accepts

* **exist:** function uses as a callback if the value was send
* **not_exist:** function uses as a callback if the value was not send
* **args:** arguments for the function callbacks

Example
~~~~~~~

.. code-block:: python

  def saving(self, user):
      user.process('phone_number', exist=self.__process_phone)
      user.errors()

  def __process_phone(self, user):
      '''
      This function process the phone if the user send one
      '''
      if user.phone[0] != "+":
        user.phone = "+1 {}".format(user.phone)
