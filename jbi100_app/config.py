# Here you can add any global configurations

# casualties
category_list1 = ["accident_year", "casualty_class", "sex_of_casualty", "age_of_casualty", "age_band_of_casualty", "casualty_severity", "pedestrian_location", "pedestrian_movement", "car_passenger", "bus_or_coach_passenger", "pedestrian_road_maintenance_worker", "casualty_type", "casualty_home_area_type", "casualty_imd_decile"]
# vehicles
category_list2 = ["accident_year", "vehicle_type", "towing_and_articulation", "vehicle_manoeuvre", "vehicle_direction_from", "vehicle_direction_to", "vehicle_location_restricted_lane", "junction_location", "skidding_and_overturning", "hit_object_in_carriageway", "vehicle_leaving_carriageway", "hit_object_off_carriageway", "first_point_of_impact", "vehicle_left_hand_drive", "journey_purpose_of_driver", "sex_of_driver", "age_of_driver", "age_band_of_driver", "engine_capacity_cc", "propulsion_code", "age_of_vehicle", "generic_make_model", "driver_imd_decile", "driver_home_area_type"]
# accident
category_list3 = ["accident_year", "accident_severity", "number_of_vehicles", "number_of_casualties", "day_of_week", "road_type", "speed_limit", "did_police_officer_attend_scene_of_accident", "urban_or_rural_area", "pedestrian_crossing_physical_facilities", "weather_conditions"]

# directories for stored .csv files
casualty_data = 'data/dft-road-casualty-statistics-casualty-1979-2020.csv'
vehicle_data = 'data/dft-road-casualty-statistics-vehicle-1979-2020.csv'
accident_data = 'data/dft-road-casualty-statistics-accident-1979-2020.csv'

num_plots = 6
