class BMI:
    @staticmethod
    def compute(weight, height):
        return weight / (height ** 2)

    @staticmethod
    def advice(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        else:
            return "Overweight"
