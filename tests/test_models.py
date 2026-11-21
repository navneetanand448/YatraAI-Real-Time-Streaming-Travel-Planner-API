import unittest

from pydantic import ValidationError

from app.model import PlaceModel, TravelPlanResponse, TravelRequestModel, WeatherResponseModel


class TravelRequestModelTests(unittest.TestCase):
    def test_normalizes_destination_and_currency(self):
        request = TravelRequestModel(
            destination="  Jaipur  ",
            start_date="2026-12-01",
            end_date="2026-12-03",
            base_currency="inr",
        )

        self.assertEqual(request.destination, "Jaipur")
        self.assertEqual(request.base_currency, "INR")

    def test_rejects_invalid_currency_code(self):
        with self.assertRaises(ValidationError):
            TravelRequestModel(
                destination="Jaipur",
                start_date="2026-12-01",
                end_date="2026-12-03",
                base_currency="US dollars",
            )

    def test_rejects_blank_destination(self):
        with self.assertRaises(ValidationError):
            TravelRequestModel(
                destination="   ",
                start_date="2026-12-01",
                end_date="2026-12-03",
            )

    def test_rejects_unknown_request_fields(self):
        with self.assertRaises(ValidationError):
            TravelRequestModel(
                destination="Jaipur",
                start_date="2026-12-01",
                end_date="2026-12-03",
                unexpected="value",
            )


class ResponseModelTests(unittest.TestCase):
    def test_rejects_out_of_range_weather_and_place_values(self):
        with self.assertRaises(ValidationError):
            WeatherResponseModel(
                date="2026-12-01",
                condition="Sunny",
                temperature_high=32,
                temperature_low=24,
                humidity=101,
                rain_chance=10,
            )

        with self.assertRaises(ValidationError):
            PlaceModel(
                name="Amber Fort",
                description="A hilltop fort",
                category="Historical Site",
                rating=5.1,
                estimated_time_hours=2,
            )

    def test_travel_plan_response_accepts_service_data(self):
        response = TravelPlanResponse(
            message="Travel plan created successfully",
            weather_data=[
                WeatherResponseModel(
                    date="2026-12-01",
                    condition="Sunny",
                    temperature_high=32,
                    temperature_low=24,
                    humidity=50,
                    rain_chance=10,
                )
            ],
            places_data=[
                PlaceModel(
                    name="Amber Fort",
                    description="A hilltop fort",
                    category="Historical Site",
                    rating=4.7,
                    estimated_time_hours=2,
                )
            ],
            currency_rates={"INR": 1.0, "USD": 0.012},
        )

        self.assertEqual(response.weather_data[0].condition, "Sunny")
        self.assertEqual(response.places_data[0].name, "Amber Fort")


if __name__ == "__main__":
    unittest.main()
