from rest_framework.throttling import AnnonRateThrottle

class Onboardingthrottle(AnnonRateThrottle):
    scope = "onboarding"
