import streamlit as st

def solve_microscope():
    st.title("🔬 Microscope Size Calculator")
    st.markdown("Enter **two** values to calculate the third. Leave the field you want to find **empty**.")

    # Input fields
    actual_input = st.text_input("Actual Object Size (e.g., µm)")
    mag_input = st.text_input("Magnification (e.g., 400)")
    img_input = st.text_input("Image/Microscope Size (e.g., mm)")

    if st.button("Calculate"):
        try:
            # Convert inputs to floats if they aren't empty
            actual = float(actual_input) if actual_input.strip() else None
            mag = float(mag_input) if mag_input.strip() else None
            img = float(img_input) if img_input.strip() else None

            # Logic check: we need exactly two values
            vals = [actual, mag, img]
            none_count = vals.count(None)

            if none_count != 1:
                st.error("Please fill in exactly TWO boxes to solve for the third.")
            else:
                # Calculations based on the formula: Mag = Image / Actual
                result = 0
                label = ""

                # Using a while loop to process logic once as requested
                calculation_done = False
                while not calculation_done:
                    if actual is None:
                        result = img / mag
                        label = f"Actual Size: {result:.4f}"
                    elif mag is None:
                        result = img / actual
                        label = f"Magnification: {result:.1f}x"
                    elif img is None:
                        result = actual * mag
                        label = f"Image Size: {result:.4f}"
                    
                    calculation_done = True

                st.success(f"### {label}")

        except ValueError:
            st.error("Please enter valid numbers only.")
        except ZeroDivisionError:
            st.error("Values cannot be zero.")

if __name__ == "__main__":
    solve_microscope()