class PhysicalActivityTracker:
    def __init__(self):
        self.recommendations = {
            "low": 30,
            "moderate": 20,
            "high": 10
        }

    def get_suggestion(self, intensity, time_minutes):
        recommended_time = self.recommendations[intensity]

        if time_minutes < recommended_time:
            return "Add more intensity or time."
        elif time_minutes > recommended_time * 1.5:
            return "Take it a bit slower."
        else:
            return "Great job!"
