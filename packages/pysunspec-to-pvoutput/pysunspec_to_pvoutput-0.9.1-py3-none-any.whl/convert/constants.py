from convert.models import DataMx

MX_POWER_GENERATION = DataMx(group_name="inverter",
                             value_id="W",
                             pvoutput_field_name="power generation")

MX_ENERGY_GENERATION = DataMx(group_name="inverter",
                              value_id="WH",
                              pvoutput_field_name="energy generation")

MX_VOLTAGE = DataMx(group_name="inverter",
                    value_id="PhVphA",
                    pvoutput_field_name="voltage")
