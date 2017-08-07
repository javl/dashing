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
			// microphone area
			translate([60-13, 0, 0])
			hull(){
				cylinder(d=1.5, h=3, $fn=180);
				translate([-2, 0, 0])
				cylinder(d=1.5, h=3, $fn=180);
			}
		}
		// hole for button
		translate([0, 0, -1])
		cylinder(d=18, h=20, $fn=180);

		// make the whole thing hollow except
		// for a button connector pin
		// for the button
		translate([0, 0, -2])
		difference(){
			hull(){
				cylinder(d=25-2, h=16, $fn=180);
				translate([60-25, 0, 0])
				cylinder(d=25-2, h=16, $fn=180);
			}
			// connector pin
			translate([35, -6, 13])
			cube([4, 12, 4]);
		}
		// hole for button
		translate([0, 0, -1])
		cylinder(d=18, h=20, $fn=180);
	}
}

module button(){
	// hole for button
	translate([0, 0, 13])
	difference(){
		union(){
			cylinder(d=18-1, h=3, $fn=180);
			hull(){
				cylinder(d=19, h=1, $fn=180);
				translate([60-25, 0, 0])
				cylinder(d=19, h=1, $fn=180);

			}
		}
		translate([0, 0, -1])
		cylinder(d=4, h=3, $fn=180);
		
		translate([35, -6, -4])
		cube([4, 12, 10]);
		
	}
	
}

module lid(){
	difference(){
		union(){
		translate([0, 0, -1])
		hull(){
			cylinder(d=25, h=2, $fn=180);
			translate([60-25, 0, 0])
			cylinder(d=25, h=2, $fn=180);
		}
		hull(){
			cylinder(d=25-2.6, h=2.4, $fn=180);
			translate([60-25, 0, 0])
			cylinder(d=25-2.6, h=2.4, $fn=180);
		}
			translate([0, 0, 2.4 + 2.5]){
				//translate([0, 0, 0])
				//cylinder(d=3, h=9.4, $fn=180);
		
				difference(){
					//button holder
					translate([-1.5-1-1.5, -7.4/2-1.5, -2.6])
					cube([12+3, 7.4+3, 5]);
				
					//button
					translate([-1.5-1, -7.4/2, 0])
					cube([12+2, 7.4, 7]);
				}
			}
		}
		translate([30-25/2, 0, -1])
		cylinder(d=4, h=10, $fn=180);
		//difference(){
			//	cube([13, 11, 7]);
			//	translate([0, 1.5, 0])
			//}
	}
}

translate([0, 0, 15])
body();
translate([0, 0, -10])
button();
translate([0, 0, -10])
lid();