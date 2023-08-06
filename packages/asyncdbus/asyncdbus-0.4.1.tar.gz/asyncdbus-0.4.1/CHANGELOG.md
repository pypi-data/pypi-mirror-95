# Changelog for asyncdbus

## Version 0.3.x

This version forks the library and converts it to anyio.

* remove aio and glib subpackages
* remove all uses of some "Future" data type
* minimal surgery to get it all to work with what will become anyio 3
* `MessageBus.connect()` is now an async context manager
* error replies now raise `DBusError`
* several methods are now async: they wait for the reply
  and may raise an error
* Add explicit typing for DBus signatures
  This should, at least in principle, allow compatibility with mypy and
  similar type checkers.

# Changelog for dbus-next

## Version 0.2.2

This version contains some bugfixes and a new feature

* Add `connected` instance variable to the `MessageBus` (#74)
* Better handling of message bus errors on disconnect (de8ed30)
* Ensure futures are not done when settings results and exceptions (#73, 1213667)

## Version 0.2.1

This version adds performance optimizations, bugfixes, and new features.

* aio.MessageBus: Support passing unix fds. (#54)
* Unmarshaller optimizations for a significant performance increase in message reading. (#62, #64)
* Cache instances of `SignatureTree`. (ace5584)
* Fix socket creation on macos. (#63)
* Implement PEP 561 to indicate inline type hints. (#69)
* aio.MessageBus: Return a future from `send()`. (302511b)
* aio.MessageBus: Add `wait_for_disconnect()` to detect connection errors. (ab01ab1)

Notice: `aio.MessageBus.send()` will be changed to a coroutine function in the 1.0 version of this library.

## Version 0.1.4

This version adds some bugfixes and new features.

* Support tcp transport addresses (#57)
* Add support for the annonymous authentication protocol (#32)
* Add flags kwarg to aio high level client method call (#55)
* Allow subclassing of DBusError (#42)
* Fix exception in aio message handler loop on task cancellation (ff165aa)
* Improve error messages (#46, #59)
* Fix match rule memory leak bug (508edf8)
* Don't add match rules for high level client by default (615218f)
* Add empty properties interface to standard interfaces (#49)

## Version 0.1.3

This version adds some bugfixes and new features.

* Add the object manager interface to the service. (#14, #37)
* Allow coroutines in service methods. (#24, #27)
* Client: don't send method replies with `NO_REPLY_EXPECTED` message flag. (#22)
* Fix duplicate nodes in introspection. (#13)

## Version 0.1.2

This version adds some bugfixes.

* Allow exporting interface multiple times (#4)
* Fix super call in exceptions (#5)
* Add timeout support on `introspect` (#7)
* Add unix fd type 'h' to valid tokens (#9)
* Dont use future annotations (#10)
* Fix variant validator (d724fc2)

## Version 0.1.1

This version adds some major features and breaking changes.

* Remove the MessageBus convenience constructors (breaking).
* Complete documentation.
* Type annotation for all public methods.

## Version 0.0.1

This is the first release of python-dbus-next.
