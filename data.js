window.SYSTEM_LIBRARY = {
 "_doc": "System-tool library. Each entry is a star_system.schema.json system, plus tool-added fields: elements may carry name and _ui:{angle}. Generated/edited via art/web/system_tool/.",
 "systems": [
  {
   "id": "system_00002",
   "name": "Solivarn",
   "system_features": [
    {
     "name": "Gravity Tides",
     "roll": 2,
     "sub_effects": [
      {
       "id": "extra_gravity_riptides",
       "description": "Add 1d5 Gravity Riptides to the System (placeable in any Solar Zone)",
       "sub_roll": 1
      }
     ],
     "_source": "src_rt14_stars_p9"
    }
   ],
   "feature_flags": {
    "inner_cauldron_weak": false,
    "inner_cauldron_dominant": false,
    "primary_biosphere_weak": false,
    "primary_biosphere_dominant": false,
    "outer_reaches_weak": false,
    "outer_reaches_dominant": false,
    "extra_asteroid_field": 0,
    "bountiful_asteroids": false,
    "extra_mineral_resources_per_planet": 0,
    "chance_for_extra_exotic_materials_per_planet": false,
    "extra_gravity_riptides": 3,
    "gravity_tides_gravity_wells_around_planets": false,
    "gravity_tides_travel_time_halves": false,
    "extra_planets_in_each_solar_zone": 0,
    "haven_thicker_atmospheres_in_primary_biosphere": false,
    "haven_better_habitability": false,
    "ill_omened_fickle_fate_points": false,
    "ill_omened_willpower_penalty": false,
    "ill_omened_doubled_insanity": false,
    "ill_omened_fear_from_psychic_exploration": false,
    "pirate_den_present": false,
    "ruined_empire_extra_xenos_ruins_on_different_planets": 0,
    "ruined_empire_increased_abundance_xenos_ruins": false,
    "ruined_empire_extra_archeotech_caches_on_different_planets": 0,
    "ruined_empire_increased_abundance_archeotech_caches": false,
    "minimum_num_planets_after_modifiers": 0,
    "starfarers_num_system_features_inhabited": 0,
    "num_planets_modifier": 0,
    "num_planets_in_warp_storms": 0,
    "warp_stasis_focus_power_penalties": false,
    "warp_stasis_no_push": false,
    "warp_stasis_reduced_psychic_phenomena": false
   },
   "star": {
    "type": "Vigorous",
    "description": "A steady illumination burns forth from the heart of this star. Its coloration is likely to be a pure white.",
    "roll": 3,
    "solar_zone_modifiers": {},
    "_source": "src_rt14_stars_p13"
   },
   "solar_zones": {
    "inner_cauldron": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "Dust Cloud",
       "roll": 33,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Radiation Bursts",
       "roll": 78,
       "count": 1,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Asteroid Cluster",
       "roll": 28,
       "_source": "src_rt14_stars_p14"
      }
     ]
    },
    "primary_biosphere": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "No Feature",
       "roll": 5,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Planet",
       "roll": 75,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Rocky Planet",
        "body_size": "Low-Mass",
        "gravity": "Low Gravity",
        "orbital_features": [
         {
          "feature_type": "Large Asteroid",
          "description": "An asteroid of unusual size has been captured by the Planet's gravity well, in a stable orbit. Large enough to be noted by an orbital survey, but not seen from the surface without visual enhancement.",
          "roll": 50,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Thin",
        "atmospheric_composition": "Tainted",
        "climate": "Temperate World",
        "habitability": "Verdant",
        "territories": [
         {
          "base_terrain": "Wasteland",
          "traits": [
           "Expansive"
          ],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Plains",
          "traits": [
           "Expansive"
          ],
          "landmarks": [
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Whirlpool",
            "category": "Exceptional"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Swamp",
          "traits": [
           "Virulent",
           "Unusual Location",
           "Roll again twice and apply both"
          ],
          "landmarks": [
           {
            "type": "Perpetual Storm",
            "category": "Exceptional"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Mountain",
          "traits": [],
          "landmarks": [
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Crater",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           }
          ]
         }
        ],
        "mineral_resources": [
         {
          "resource_type": "Radioactive",
          "abundance": {
           "level": "Sustainable",
           "roll_result": 60
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Ornamental",
          "abundance": {
           "level": "Significant",
           "roll_result": 73
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Radioactive",
          "abundance": {
           "level": "Major",
           "roll_result": 93
          },
          "_source": "src_rt14_stars_p29"
         }
        ],
        "additional_resources": [],
        "native_species": [
         {
          "archetype": "Shadowed Stalker",
          "natures": [
           "Chameleonic"
          ]
         },
         {
          "archetype": "Ptera-Beast",
          "natures": [
           "Doom Diver"
          ]
         },
         {
          "archetype": "Venomous Terror",
          "natures": [
           "Hidden Death"
          ]
         },
         {
          "archetype": "Shadowed Stalker",
          "natures": [
           "Deadly Ambusher"
          ]
         }
        ],
        "inhabitants": {
         "species": "Kroot",
         "development": "Colony"
        },
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Planet",
       "roll": 88,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Rocky Planet",
        "body_size": "Vast",
        "gravity": "High Gravity",
        "orbital_features": [
         {
          "feature_type": "Moon",
          "description": "A true moon, generated as a Planet (Planet Creation p.19). Normally cannot have a higher Planetary Body than its parent. A moon never generates its own Orbital Features.",
          "roll": 94,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "An orbital body between an extremely large asteroid and a very small moon. Limited gravity well allows low-gravity travel (RT Core p.269). Roll 1d10; on 6+ it counts as a Resource — roll once on Table 1-20: Mineral Resources and once on Table 1-19 (Abundance) at -5.",
          "roll": 89,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "An orbital body between an extremely large asteroid and a very small moon. Limited gravity well allows low-gravity travel (RT Core p.269). Roll 1d10; on 6+ it counts as a Resource — roll once on Table 1-20: Mineral Resources and once on Table 1-19 (Abundance) at -5.",
          "roll": 86,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "An orbital body between an extremely large asteroid and a very small moon. Limited gravity well allows low-gravity travel (RT Core p.269). Roll 1d10; on 6+ it counts as a Resource — roll once on Table 1-20: Mineral Resources and once on Table 1-19 (Abundance) at -5.",
          "roll": 63,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Moderate",
        "atmospheric_composition": "Toxic",
        "climate": "Cold World",
        "habitability": "Inhospitable",
        "territories": [
         {
          "base_terrain": "Plains",
          "traits": [
           "Broken Ground",
           "Extreme Temperature",
           "Unusual Location",
           "Broken Ground"
          ],
          "landmarks": [
           {
            "type": "Glacier",
            "category": "Exceptional"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Glacier",
            "category": "Exceptional"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Wasteland",
          "traits": [
           "Unusual Location"
          ],
          "landmarks": [
           {
            "type": "Whirlpool",
            "category": "Exceptional"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Mountain",
          "traits": [],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Mountain",
          "traits": [],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Glacier",
            "category": "Exceptional"
           }
          ]
         },
         {
          "base_terrain": "Plains",
          "traits": [
           "Expansive",
           "Expansive"
          ],
          "landmarks": [
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Glacier",
            "category": "Exceptional"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Glacier",
            "category": "Exceptional"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Mountain",
          "traits": [],
          "landmarks": [
           {
            "type": "Glacier",
            "category": "Exceptional"
           },
           {
            "type": "Crater",
            "category": "General"
           },
           {
            "type": "Crater",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Crater",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Swamp",
          "traits": [
           "Roll again twice and apply both",
           "Virulent",
           "Virulent",
           "Expansive"
          ],
          "landmarks": [
           {
            "type": "Reef",
            "category": "Exceptional"
           },
           {
            "type": "Inland Sea",
            "category": "Exceptional"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Perpetual Storm",
            "category": "Exceptional"
           }
          ]
         },
         {
          "base_terrain": "Forest",
          "traits": [
           "Notable Species"
          ],
          "landmarks": [
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Reef",
            "category": "Exceptional"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           }
          ]
         }
        ],
        "mineral_resources": [
         {
          "resource_type": "Ornamental",
          "abundance": {
           "level": "Limited",
           "roll_result": 34
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Ornamental",
          "abundance": {
           "level": "Significant",
           "roll_result": 78
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Ornamental",
          "abundance": {
           "level": "Significant",
           "roll_result": 84
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Industrial Metal",
          "abundance": {
           "level": "Major",
           "roll_result": 90
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Radioactive",
          "abundance": {
           "level": "Limited",
           "roll_result": 18
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Industrial Metal",
          "abundance": {
           "level": "Limited",
           "roll_result": 33
          },
          "_source": "src_rt14_stars_p29"
         }
        ],
        "additional_resources": [
         {
          "resource_type": "Archeotech Cache",
          "abundance": {
           "level": "Limited",
           "roll_result": 17
          },
          "_source": "src_rt14_stars_p27"
         }
        ],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Asteroid Belt",
       "roll": 21,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Dust Cloud",
       "roll": 56,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Gravity Riptide",
       "roll": null,
       "_source": "src_rt14_stars_p9_gravity_tides_feature"
      },
      {
       "element_type": "Gravity Riptide",
       "roll": null,
       "_source": "src_rt14_stars_p9_gravity_tides_feature"
      }
     ]
    },
    "outer_reaches": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "Planet",
       "roll": 93,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Rocky Planet",
        "body_size": "Small",
        "gravity": "Normal Gravity",
        "orbital_features": [
         {
          "feature_type": "Lesser Moon",
          "description": "An orbital body between an extremely large asteroid and a very small moon. Limited gravity well allows low-gravity travel (RT Core p.269). Roll 1d10; on 6+ it counts as a Resource — roll once on Table 1-20: Mineral Resources and once on Table 1-19 (Abundance) at -5.",
          "roll": 66,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "None",
        "atmospheric_composition": "N/A",
        "climate": "Ice World",
        "habitability": "Inhospitable",
        "territories": [],
        "mineral_resources": [],
        "additional_resources": [
         {
          "resource_type": "Archeotech Cache",
          "abundance": {
           "level": "Limited",
           "roll_result": 33
          },
          "_source": "src_rt14_stars_p27"
         }
        ],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Gas Giant",
       "roll": 66,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Gas Giant",
        "body_size": "Gas Giant",
        "gravity": "Titanic",
        "orbital_features": [
         {
          "feature_type": "Moon",
          "description": "Generated as a Planet (page 19). Cannot have higher Planetary Body than parent. Never generates its own Orbital Features.",
          "roll": 100,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "Roll 1d10; on 6+ houses sufficient mineral wealth to count as a Resource — roll once on Table 1-20 and determine Abundance by rolling 5d10+5.",
          "roll": 85,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "Roll 1d10; on 6+ houses sufficient mineral wealth to count as a Resource — roll once on Table 1-20 and determine Abundance by rolling 5d10+5.",
          "roll": 66,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Moon",
          "description": "Generated as a Planet (page 19). Cannot have higher Planetary Body than parent. Never generates its own Orbital Features.",
          "roll": 98,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Moon",
          "description": "Generated as a Planet (page 19). Cannot have higher Planetary Body than parent. Never generates its own Orbital Features.",
          "roll": 100,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Planetary Rings (Debris)",
          "description": "Narrow band of asteroids/ice. Direct passage requires Challenging (+0) Pilot (Space Craft)+Manoeuvrability as if Asteroid Field (RT Core p.226-227). Multiple instances stack: -10 to passage tests per additional instance.",
          "roll": 31,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Planetary Rings (Dust)",
          "description": "Wide ring of fine particles. Auger tests through the ring are two steps more difficult. Multiple instances increase the existing Rings; -5 additional auger-penalty for every two additional instances.",
          "roll": 50,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Planetary Rings (Debris)",
          "description": "Narrow band of asteroids/ice. Direct passage requires Challenging (+0) Pilot (Space Craft)+Manoeuvrability as if Asteroid Field (RT Core p.226-227). Multiple instances stack: -10 to passage tests per additional instance.",
          "roll": 35,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "Roll 1d10; on 6+ houses sufficient mineral wealth to count as a Resource — roll once on Table 1-20 and determine Abundance by rolling 5d10+5.",
          "roll": 80,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "Roll 1d10; on 6+ houses sufficient mineral wealth to count as a Resource — roll once on Table 1-20 and determine Abundance by rolling 5d10+5.",
          "roll": 83,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Lesser Moon",
          "description": "Roll 1d10; on 6+ houses sufficient mineral wealth to count as a Resource — roll once on Table 1-20 and determine Abundance by rolling 5d10+5.",
          "roll": 51,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Planetary Rings (Dust)",
          "description": "Wide ring of fine particles. Auger tests through the ring are two steps more difficult. Multiple instances increase the existing Rings; -5 additional auger-penalty for every two additional instances.",
          "roll": 45,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Moon",
          "description": "Generated as a Planet (page 19). Cannot have higher Planetary Body than parent. Never generates its own Orbital Features.",
          "roll": 96,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "Moon",
          "description": "Generated as a Planet (page 19). Cannot have higher Planetary Body than parent. Never generates its own Orbital Features.",
          "roll": 100,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Thin",
        "atmospheric_composition": "Toxic",
        "climate": "Cold World",
        "habitability": "Inhospitable",
        "territories": [],
        "mineral_resources": [],
        "additional_resources": [],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Dust Cloud",
       "roll": 48,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Gas Giant",
       "roll": 70,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Gas Giant",
        "body_size": "Gas Dwarf",
        "gravity": "Low Gravity",
        "orbital_features": [
         {
          "feature_type": "No Features",
          "description": "No notable features are added to the Planet's orbit.",
          "roll": 1,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Moderate",
        "atmospheric_composition": "Pure",
        "climate": "Ice World",
        "habitability": "Inhospitable",
        "territories": [
         {
          "base_terrain": "Swamp",
          "traits": [
           "Virulent"
          ],
          "landmarks": [
           {
            "type": "Reef",
            "category": "Exceptional"
           },
           {
            "type": "Mountain",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Wasteland",
          "traits": [
           "Notable Species"
          ],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Forest",
          "traits": [
           "Notable Species",
           "Exotic Nature",
           "Unique Compound"
          ],
          "landmarks": [
           {
            "type": "Perpetual Storm",
            "category": "Exceptional"
           }
          ]
         },
         {
          "base_terrain": "Plains",
          "traits": [
           "Extreme Temperature",
           "Broken Ground"
          ],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Crater",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Forest",
          "traits": [
           "Expansive",
           "Notable Species",
           "Unusual Location"
          ],
          "landmarks": [
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Whirlpool",
            "category": "Exceptional"
           },
           {
            "type": "Canyon",
            "category": "General"
           }
          ]
         }
        ],
        "mineral_resources": [],
        "additional_resources": [],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Gravity Riptide",
       "roll": null,
       "_source": "src_rt14_stars_p9_gravity_tides_feature"
      }
     ]
    }
   },
   "_generated_by": "rogue_trader.rules.star_system_generation",
   "_generated_at": "2026-06-12T16:28:34.464023Z",
   "_seed": 2,
   "_source": "src_rt14_stars_p7"
  },
  {
   "id": "system_00007",
   "name": "System 00007",
   "system_features": [
    {
     "name": "Haven",
     "roll": 3,
     "sub_effects": [
      {
       "id": "thicker_atmospheres",
       "description": "Primary Biosphere planets have thicker atmospheres (roll Table 1-9 with +2)",
       "sub_roll": 2
      }
     ],
     "_source": "src_rt14_stars_p9"
    }
   ],
   "feature_flags": {
    "inner_cauldron_weak": false,
    "inner_cauldron_dominant": true,
    "primary_biosphere_weak": true,
    "primary_biosphere_dominant": false,
    "outer_reaches_weak": false,
    "outer_reaches_dominant": false,
    "extra_asteroid_field": 0,
    "bountiful_asteroids": false,
    "extra_mineral_resources_per_planet": 0,
    "chance_for_extra_exotic_materials_per_planet": false,
    "extra_gravity_riptides": 0,
    "gravity_tides_gravity_wells_around_planets": false,
    "gravity_tides_travel_time_halves": false,
    "extra_planets_in_each_solar_zone": 0,
    "haven_thicker_atmospheres_in_primary_biosphere": true,
    "haven_better_habitability": false,
    "ill_omened_fickle_fate_points": false,
    "ill_omened_willpower_penalty": false,
    "ill_omened_doubled_insanity": false,
    "ill_omened_fear_from_psychic_exploration": false,
    "pirate_den_present": false,
    "ruined_empire_extra_xenos_ruins_on_different_planets": 0,
    "ruined_empire_increased_abundance_xenos_ruins": false,
    "ruined_empire_extra_archeotech_caches_on_different_planets": 0,
    "ruined_empire_increased_abundance_archeotech_caches": false,
    "minimum_num_planets_after_modifiers": 0,
    "starfarers_num_system_features_inhabited": 0,
    "num_planets_modifier": 0,
    "num_planets_in_warp_storms": 0,
    "warp_stasis_focus_power_penalties": false,
    "warp_stasis_no_push": false,
    "warp_stasis_reduced_psychic_phenomena": false
   },
   "star": {
    "type": "Mighty",
    "description": "The fierce light of this star dominates its system utterly. Its coloration is likely to be blue or blue-white. The Inner Cauldron is dominant, and the Primary Biosphere is weak.",
    "roll": 1,
    "solar_zone_modifiers": {
     "inner_cauldron": "dominant",
     "primary_biosphere": "weak"
    },
    "_source": "src_rt14_stars_p13"
   },
   "solar_zones": {
    "inner_cauldron": {
     "size": "dominant",
     "element_count_formula": "1d5+2",
     "elements": [
      {
       "element_type": "Planet",
       "roll": 69,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Rocky Planet",
        "body_size": "Small",
        "gravity": "Low Gravity",
        "orbital_features": [
         {
          "feature_type": "Lesser Moon",
          "description": "An orbital body between an extremely large asteroid and a very small moon. Limited gravity well allows low-gravity travel (RT Core p.269). Roll 1d10; on 6+ it counts as a Resource — roll once on Table 1-20: Mineral Resources and once on Table 1-19 (Abundance) at -5.",
          "roll": 61,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Moderate",
        "atmospheric_composition": "Deadly",
        "climate": "Temperate World",
        "habitability": "Inhospitable",
        "territories": [],
        "mineral_resources": [],
        "additional_resources": [
         {
          "resource_type": "Archeotech Cache",
          "abundance": {
           "level": "Significant",
           "roll_result": 74
          },
          "_source": "src_rt14_stars_p27"
         },
         {
          "resource_type": "Xenos Ruins",
          "abundance": {
           "level": "Sustainable",
           "roll_result": 51
          },
          "_source": "src_rt14_stars_p27",
          "details": {
           "xenos_origin": "Undiscovered species"
          }
         }
        ],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "No Feature",
       "roll": 13,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Gravity Riptide",
       "roll": 47,
       "_source": "src_rt14_stars_p14"
      }
     ]
    },
    "primary_biosphere": {
     "size": "weak",
     "element_count_formula": "1d5-2 (minimum 1)",
     "elements": [
      {
       "element_type": "No Feature",
       "roll": 8,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "Planet",
       "roll": 65,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Rocky Planet",
        "body_size": "Small and Dense",
        "gravity": "Low Gravity",
        "orbital_features": [
         {
          "feature_type": "No Features",
          "description": "No notable features are added to the Planet's orbit.",
          "roll": 8,
          "_source": "src_rt14_stars_p20"
         },
         {
          "feature_type": "No Features",
          "description": "No notable features are added to the Planet's orbit.",
          "roll": 28,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Moderate",
        "atmospheric_composition": "Toxic",
        "climate": "Cold World",
        "habitability": "Inhospitable",
        "territories": [
         {
          "base_terrain": "Wasteland",
          "traits": [
           "Notable Species",
           "Unusual Location"
          ],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           }
          ]
         }
        ],
        "mineral_resources": [
         {
          "resource_type": "Ornamental",
          "abundance": {
           "level": "Minimal",
           "roll_result": 13
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Radioactive",
          "abundance": {
           "level": "Major",
           "roll_result": 92
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Industrial Metal",
          "abundance": {
           "level": "Significant",
           "roll_result": 73
          },
          "_source": "src_rt14_stars_p29"
         }
        ],
        "additional_resources": [],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Asteroid Belt",
       "roll": 28,
       "_source": "src_rt14_stars_p14"
      }
     ]
    },
    "outer_reaches": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "No Feature",
       "roll": 12,
       "_source": "src_rt14_stars_p14"
      }
     ]
    }
   },
   "_generated_by": "rogue_trader.rules.star_system_generation",
   "_generated_at": "2026-06-12T16:31:09.753645Z",
   "_seed": 7,
   "_source": "src_rt14_stars_p7"
  },
  {
   "id": "system_00013",
   "name": "System 00013",
   "system_features": [
    {
     "name": "Pirate Den",
     "roll": 5,
     "sub_effects": [
      {
       "id": "spawn_pirate_fleet",
       "description": "1d5+4 Wolfpack Raiders led by a stronger flagship (often a Frigate). Never <5, rarely >8. Alternative fleets: Ork/Eldar/Rak'Gol/Chaos vessels of higher quality."
      }
     ],
     "_source": "src_rt14_stars_p9"
    }
   ],
   "feature_flags": {
    "inner_cauldron_weak": false,
    "inner_cauldron_dominant": false,
    "primary_biosphere_weak": false,
    "primary_biosphere_dominant": false,
    "outer_reaches_weak": false,
    "outer_reaches_dominant": false,
    "extra_asteroid_field": 0,
    "bountiful_asteroids": false,
    "extra_mineral_resources_per_planet": 0,
    "chance_for_extra_exotic_materials_per_planet": false,
    "extra_gravity_riptides": 0,
    "gravity_tides_gravity_wells_around_planets": false,
    "gravity_tides_travel_time_halves": false,
    "extra_planets_in_each_solar_zone": 0,
    "haven_thicker_atmospheres_in_primary_biosphere": false,
    "haven_better_habitability": false,
    "ill_omened_fickle_fate_points": false,
    "ill_omened_willpower_penalty": false,
    "ill_omened_doubled_insanity": false,
    "ill_omened_fear_from_psychic_exploration": false,
    "pirate_den_present": true,
    "ruined_empire_extra_xenos_ruins_on_different_planets": 0,
    "ruined_empire_increased_abundance_xenos_ruins": false,
    "ruined_empire_extra_archeotech_caches_on_different_planets": 0,
    "ruined_empire_increased_abundance_archeotech_caches": false,
    "minimum_num_planets_after_modifiers": 0,
    "starfarers_num_system_features_inhabited": 0,
    "num_planets_modifier": 0,
    "num_planets_in_warp_storms": 0,
    "warp_stasis_focus_power_penalties": false,
    "warp_stasis_no_push": false,
    "warp_stasis_reduced_psychic_phenomena": false
   },
   "star": {
    "type": "Vigorous",
    "description": "A steady illumination burns forth from the heart of this star. Its coloration is likely to be a pure white.",
    "roll": 3,
    "solar_zone_modifiers": {},
    "_source": "src_rt14_stars_p13"
   },
   "solar_zones": {
    "inner_cauldron": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "Radiation Bursts",
       "roll": 86,
       "count": 1,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "No Feature",
       "roll": 19,
       "_source": "src_rt14_stars_p14"
      }
     ]
    },
    "primary_biosphere": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "Planet",
       "roll": 83,
       "_source": "src_rt14_stars_p14",
       "details": {
        "body_class": "Rocky Planet",
        "body_size": "Vast",
        "gravity": "Normal Gravity",
        "orbital_features": [
         {
          "feature_type": "No Features",
          "description": "No notable features are added to the Planet's orbit.",
          "roll": 4,
          "_source": "src_rt14_stars_p20"
         }
        ],
        "atmospheric_presence": "Moderate",
        "atmospheric_composition": "Toxic",
        "climate": "Cold World",
        "habitability": "Inhospitable",
        "territories": [
         {
          "base_terrain": "Plains",
          "traits": [
           "Expansive"
          ],
          "landmarks": [
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Reef",
            "category": "Exceptional"
           },
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Swamp",
          "traits": [
           "Unusual Location",
           "Stagnant",
           "Virulent",
           "Stagnant"
          ],
          "landmarks": [
           {
            "type": "Perpetual Storm",
            "category": "Exceptional"
           },
           {
            "type": "Glacier",
            "category": "Exceptional"
           },
           {
            "type": "Crater",
            "category": "General"
           },
           {
            "type": "Perpetual Storm",
            "category": "Exceptional"
           },
           {
            "type": "Reef",
            "category": "Exceptional"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Inland Sea",
            "category": "Exceptional"
           }
          ]
         },
         {
          "base_terrain": "Swamp",
          "traits": [
           "Unusual Location",
           "Extreme Temperature",
           "Notable Species"
          ],
          "landmarks": [
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           }
          ]
         },
         {
          "base_terrain": "Swamp",
          "traits": [
           "Virulent",
           "Notable Species"
          ],
          "landmarks": [
           {
            "type": "Canyon",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Mountain",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           },
           {
            "type": "Volcano",
            "category": "General"
           },
           {
            "type": "Cave Network",
            "category": "General"
           }
          ]
         }
        ],
        "mineral_resources": [
         {
          "resource_type": "Industrial Metal",
          "abundance": {
           "level": "Minimal",
           "roll_result": 10
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Ornamental",
          "abundance": {
           "level": "Significant",
           "roll_result": 84
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Radioactive",
          "abundance": {
           "level": "Sustainable",
           "roll_result": 50
          },
          "_source": "src_rt14_stars_p29"
         },
         {
          "resource_type": "Industrial Metal",
          "abundance": {
           "level": "Major",
           "roll_result": 93
          },
          "_source": "src_rt14_stars_p29"
         }
        ],
        "additional_resources": [
         {
          "resource_type": "Archeotech Cache",
          "abundance": {
           "level": "Limited",
           "roll_result": 29
          },
          "_source": "src_rt14_stars_p27"
         },
         {
          "resource_type": "Minerals",
          "abundance": {
           "level": "Sustainable",
           "roll_result": 64
          },
          "_source": "src_rt14_stars_p27"
         }
        ],
        "native_species": [],
        "inhabitants": null,
        "_source": "src_rt14_stars_p19"
       }
      },
      {
       "element_type": "Starship Graveyard",
       "roll": 94,
       "_source": "src_rt14_stars_p14",
       "details": {
        "origin": "Skirmish",
        "origin_roll": 90,
        "origin_description": "Elements from two different battlefleets clashed here, with each leaving behind a handful of their complement. The graveyard consists of 1d5+3 hulks. Roughly half of the ships came from each side.",
        "_source": "src_rt14_stars_p17",
        "ship_count": 7,
        "ship_count_formula": "1d5+3",
        "hulks": [
         {
          "race": "Human",
          "ship_name": "Goliath-class Factory Ship",
          "ship_class": "Transport",
          "book": "RT09_BFK",
          "page": 29,
          "upgrades": [],
          "integrity": "Damaged",
          "_roll": 53,
          "_book_source_chosen_by_random_30pct_into_the_storm": false,
          "_source": "src_rt01_core + src_rt09_battlefleet_koronus + src_rt04_into_the_storm"
         },
         {
          "race": "Other",
          "ship_name": "Unknown Other Vessel",
          "ship_class": "Frigate",
          "book": "RT09_BFK",
          "page": 0,
          "upgrades": [],
          "integrity": "Damaged",
          "_roll": null,
          "_source": "src_codifier_placeholder_for_other",
          "_note": "BFK does not catalogue Other hulls in detail. Replace with custom NPC ship as needed."
         },
         {
          "race": "Human",
          "ship_name": "Lunar-class Cruiser",
          "ship_class": "Cruiser",
          "book": "RT01_Core",
          "page": 196,
          "upgrades": [],
          "integrity": "Damaged",
          "_roll": 48,
          "_book_source_chosen_by_random_30pct_into_the_storm": false,
          "_source": "src_rt01_core + src_rt09_battlefleet_koronus + src_rt04_into_the_storm"
         },
         {
          "race": "DarkEldar",
          "ship_name": "Corsair-class Escort",
          "ship_class": "Raider",
          "book": "RT12_TSR",
          "page": 137,
          "upgrades": [],
          "integrity": "Heavily Damaged",
          "_roll": 31,
          "_source": "src_rt12_soul_reaver_p137"
         },
         {
          "race": "Human",
          "ship_name": "Jericho-class Pilgrim Vessel",
          "ship_class": "Transport",
          "book": "RT01_Core",
          "page": 194,
          "upgrades": [],
          "integrity": "Mostly Intact",
          "_roll": 6,
          "_book_source_chosen_by_random_30pct_into_the_storm": false,
          "_source": "src_rt01_core + src_rt09_battlefleet_koronus + src_rt04_into_the_storm"
         },
         {
          "race": "Ork",
          "ship_name": "Terror Ship",
          "ship_class": "Cruiser",
          "book": "RT09_BFK",
          "page": 79,
          "upgrades": [
           "Dakka Kontrol",
           "'Uge Armour Plates"
          ],
          "integrity": "Shattered",
          "_roll": 75,
          "_secondary_roll": 10,
          "_source": "src_rt09_battlefleet_koronus_p79_to_p83"
         },
         {
          "race": "Human",
          "ship_name": "Secutor-class Monitor-cruiser",
          "ship_class": "LightCruiser",
          "book": "RT04_ItS",
          "page": 152,
          "upgrades": [],
          "integrity": "Damaged",
          "_roll": 72,
          "_book_source_chosen_by_random_30pct_into_the_storm": true,
          "_source": "src_rt04_into_the_storm"
         }
        ],
        "num_resource_finds": 0,
        "resource_finds": []
       }
      }
     ]
    },
    "outer_reaches": {
     "size": "typical",
     "element_count_formula": "1d5",
     "elements": [
      {
       "element_type": "No Feature",
       "roll": 17,
       "_source": "src_rt14_stars_p14"
      },
      {
       "element_type": "No Feature",
       "roll": 10,
       "_source": "src_rt14_stars_p14"
      }
     ]
    }
   },
   "_generated_by": "rogue_trader.rules.star_system_generation",
   "_generated_at": "2026-06-12T16:31:09.783140Z",
   "_seed": 13,
   "_source": "src_rt14_stars_p7"
  }
 ]
};
