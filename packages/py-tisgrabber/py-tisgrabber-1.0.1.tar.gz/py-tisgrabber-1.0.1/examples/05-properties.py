from tisgrabber.wrapper import ImageControl

ic = ImageControl()
grabber = ic.show_device_selection_dialog()

state = {True: "on", False: "off"}

if ic.is_dev_valid(grabber):
    # Turn auto exposure on
    ic.set_property_switch(grabber, "Exposure", "Auto", True)
    on = ic.get_property_switch(grabber, "Exposure", "Auto")
    print(f"Automatic exposure is {state[on]}.")

    # Turn auto exposure off
    ic.set_property_switch(grabber, "Exposure", "Auto", False)
    on = ic.get_property_switch(grabber, "Exposure", "Auto")
    print(f"Automatic exposure is {state[on]}.")

    # Set exposure to 30 ms or its closest possible value
    ic.set_property_absolute_value(grabber, "Exposure", "Value", 0.03)
    value = ic.get_property_absolute_value(grabber, "Exposure", "Value")
    print(f"Exposure is {1e3 * value} ms.")

    # Query possible exposure values
    min_exposure, max_exposure = ic.get_property_absolute_value_range(
        grabber, "Exposure", "Value"
    )
    print(
        f"Exposure can be set between {1e3 * min_exposure} and {1e3 * max_exposure} ms."
    )

    # Query possible exposure register values
    min_exp_reg, max_exp_reg = ic.get_exp_reg_val_range(grabber)
    print(f"Exposure register values msut be between {min_exp_reg} and {max_exp_reg}.")
    exp_reg = ic.get_exp_reg_val(grabber)
    print(f"Current exposure register value is {exp_reg}.")
    set_to = -12
    ic.set_exp_reg_val(grabber, set_to)
    exp_reg = ic.get_exp_reg_val(grabber)
    print(f"After setting exposure register value to {set_to} it is is {exp_reg}.")

    # Query possible gain setting values
    min_gain, max_gain = ic.get_property_value_range(grabber, "Gain", "Value")
    gain = ic.get_property_value(grabber, "Gain", "Value")
    print(f"Gain is {gain} and can be set between {min_gain} and {max_gain}.")

    # Perform the one push  for Focus
    ic.property_one_push(grabber, "Focus")

else:
    ic.msg_box("No device opened.", "Setting and getting properties")
ic.release_grabber(grabber)
