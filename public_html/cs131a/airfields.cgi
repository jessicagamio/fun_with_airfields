#!/students/rchan85/myenvs/myenv/bin/python3

import cgi
import cgitb
cgitb.enable()

import pathlib
MYPYLABSPATH = pathlib.Path.home().joinpath('mypylabs')
import sys
sys.path.append(str(MYPYLABSPATH))

import myairfieldpack
from myairfieldpack import airport_tables
from myairfieldpack import distance_and_labels

form=cgi.FieldStorage()

code_default = 'sfo'
unit_default = 'mi'

dep_input=form.getfirst('departurecode', code_default)
arr_input=form.getfirst('arrivalcode', code_default)

dep_code=airport_tables.search_airfield(dep_input, airport_tables.MYDBNAME) + " airport"
arr_code=airport_tables.search_airfield(arr_input, airport_tables.MYDBNAME) + " airport"

dep_location=distance_and_labels.airfield_location(dep_code)
arr_location=distance_and_labels.airfield_location(arr_code)

dep_lat, dep_lon=distance_and_labels.lat_lon(dep_location)
arr_lat, arr_lon=distance_and_labels.lat_lon(arr_location)

dep_name=airport_tables.search_airfield_name(dep_input, airport_tables.MYDBNAME)
arr_name=airport_tables.search_airfield_name(arr_input, airport_tables.MYDBNAME)

unit=form.getfirst('input_measurement', unit_default)

distance=distance_and_labels.airfield_distance(unit, (dep_lat, dep_lon), (arr_lat, arr_lon))


PAGE=f"""
<html>

   <head>
   <title> Fun with Airfields </title>
   </head></font>
   <body bgcolor='white'>
    <table style="width:50%">
    <tr>
    <td></td>
    <td>
    <img src='images/snoopy_ace_flying.png' width='240pt'>
    </td>
    <td></td>
    </tr>
    <tr>
    <td>
    </td>
    <td> <font face="Comic Sans MS">
    <h1>Let's take a trip! </h1></font><br><br>
    </td>
    <td></td>
    </tr>
    <tr>
    <form>
    <td>
       <font face="Comic Sans MS"><h2> <b>Departure airfield code:</b></h2></font>
       <input type='text' name='departurecode'>
     </td> 
     <td>
      <img src='images/arrow.jpg'  width='500pt'>
     </td>
     <td>
	     <font face="Comic Sans MS"><h2> <b> Arrival airfield code: </b></h2></font>
       <input type='text' name='arrivalcode'>
     </td>
     </tr>
     </table>
       <p><font face="Comic Sans MS">
       <h2>Choose a unit of measurement for your travels! <img src='images/woodstock.png' width='40pt'></h2></font>
       </p><p> 
       <font face="Comic Sans MS">
       <h3>
          <input type="radio" name="input_measurement" value="mi"> miles <br>
          <input type='radio' name='input_measurement' value="km"> kilometers <br>
          <input type='radio' name='input_measurement' value="m"> meters <br>
          <input type='radio' name='input_measurement' value="nm"> nautical miles <br><br>
          <input type='submit' name='submit' value='Lets Go!'>
       </h3> 
       </font>
       </p>
       </form>
       <p>
       <table >
       <tr>
       <td>
      <br>
       <img src='images/snoopy_ace_rest.png' width='200pt' ><br>
       </td>
       <td>
       <font face="Comic Sans MS">
       <h1> Snoopy will fly {distance:0.2f} {unit} from {dep_name} to {arr_name} </h1></font>
       </td>
       </tr>
       </table>
       </p>  

   </body>
</html>
"""

print(PAGE)