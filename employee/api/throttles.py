from rest_framework.throttling import AnonRateThrottle

class Onboardingthrottle(AnonRateThrottle):
    scope = "onboarding"
