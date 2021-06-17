"""
This file is here for the purposes of prototyping the verification workers
it currently serves solely as a working example, but it should be eliminated
as soon as the functionality is implemented in the application
"""

from VerificationWorker.tasks import get_first_user


u = get_first_user.delay()
print(u.get(timeout=1))
