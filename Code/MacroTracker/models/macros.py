class FoodItem:
    def __init__(self, name, calories, carbs, sugar, fiber, protein, fat, water, grams):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.sugar = sugar
        self.fiber = fiber
        self.protein = protein
        self.fat = fat
        self.water = water
        self.grams = grams

    def compute_scaled(self):
        m = self.grams / 100
        return FoodItem(
            self.name,
            self.calories * m,
            self.carbs * m,
            self.sugar * m,
            self.fiber * m,
            self.protein * m,
            self.fat * m,
            self.water * m,
            self.grams
        )
