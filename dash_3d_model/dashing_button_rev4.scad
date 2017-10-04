//=====================================================
// This is a simple replica of an Amazon Dash button. After
// printing, a momentary switch with 9mm shaft can be inserted
// and hooked up to your favorite microcontroller or other
// device to track its state.
//
// Made by Jasper van Loenen for the Dashing Button
// https://jaspervanloenen.com/dashing-button
//
// Feel free to use this model in any way you like. Letting
// me know what you use it for would be appreciated.
//=====================================================

// the main body
body();
// the thinner, movable button part
pressable_button();
// the bottom part of the button
bottom();

//===============================
// The main body of the button
//===============================
module body(){
	difference(){
		// main shape
		hull(){
			cylinder(d=25, h=16, $fn=180);
			translate([60-25, 0, 0])
			cylinder(d=25, h=16, $fn=180);
		}
		// top inset
		translate([0, 0, 16-0.4])
		difference(){
			hull(){
				cylinder(d=25-2, h=0.5, $fn=180);
				translate([60-25, 0, 0])
				cylinder(d=25-2, h=0.5, $fn=180);
			}
			// ridge around button
			cylinder(d=20, h=2, $fn=180);
			// ridge around microphone area
			translate([60-13, 0, 0])
			hull(){
				cylinder(d=1.5, h=3, $fn=180);
				translate([-2, 0, 0])
				cylinder(d=1.5, h=3, $fn=180);
			}
		}
		
		// hole for the button
		translate([0, 0, -1])
		cylinder(d=18, h=20, $fn=180);

		// make the whole thing hollow except for a pin
		// to connect the movable button to
		translate([0, 0, -2])
		difference(){
			hull(){
				cylinder(d=25-3.9, h=16, $fn=180);
				translate([60-25, 0, 0])
				cylinder(d=25-3.9, h=16, $fn=180);
			}
			// connector pin
			translate([35, 0, 13.5])
			cylinder(d=10, h=4, $fn=180);
		}
	}
}

//===============================
// The movable part of the button
//===============================
module pressable_button(){
	translate([0, 0, 13])
	difference(){
		// the main part of the button
		union(){
			cylinder(d=18-1, h=3, $fn=180);
			translate([0, 0, -0.5])

			hull(){
				cylinder(d=19, h=1.5, $fn=180);
				translate([60-25, 0, 0])
				cylinder(d=19, h=1.5, $fn=180);

			}
		}
		// make an indent for the momentary switch to catch on to
		// might not be necessary, but seems to work well
		translate([0, 0, -1])
		cylinder(d=4, h=3, $fn=180);
		
		// make a hole for the connector pin on the main body
		translate([35, 0, -3])
		cylinder(d=10, h=5, $fn=180);
	}
}

//===============================
// The bottom part
//===============================
module bottom(){
	difference(){
		union(){
			// widest bottom part
			translate([0, 0, -1])
			hull(){
				cylinder(d=25, h=2, $fn=180);
				translate([60-25, 0, 0])
				cylinder(d=25, h=2, $fn=180);
			}
			// standing edge that snaps to the main body
			difference(){
				hull(){
					cylinder(d=25-4, h=1+3, $fn=180);
					translate([60-25, 0, 0])
					cylinder(d=25-4, h=1+3, $fn=180);
				}
				hull(){
					cylinder(d=25-4-4, h=3+3, $fn=180);
					translate([60-25, 0, 0])
					cylinder(d=25-4-4, h=3+3, $fn=180);
				}
	
			}
			
			// Holder for a momentary switch button (with
			// long shaft)
			translate([0, 0, 2.4 + 2.5 - 2]){
				difference(){
					//button holder
					translate([-1.5-1-1.5, -7.4/2-1.5, -2.6])
					cube([12, 7.4+3, 5+2]);
						
					//button
					translate([-1.5-1, -7.4/2, 2])
					cube([12+2, 7.4, 7]);
				}
			}
		}
		
		// make two holes for wires / screws
		translate([26-25/2, 0, -2])
		cylinder(d=5, h=10, $fn=180);
		
		translate([40-25/2, 0, -2])
		cylinder(d=5, h=10, $fn=180);
	}
}