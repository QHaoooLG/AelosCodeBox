Blockly.Blocks['1632297702511'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297702511",
      "message0": "Left3move_04253",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297702511'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,45,65,65,65,65,30,30,30,45,65,65,65,65,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 100, 100, 93, 55, 124, 100, 100, 15, 100, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(20,20,20,85,85,95,85,85,20,20,20,85,85,95,85,85,0,0,0)\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 100, 90, 93, 54, 124, 90, 100, 15, 100, 110, 107, 146, 76, 100, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 100, 95, 93, 54, 124, 105, 100, 15, 100, 106, 107, 146, 76, 115, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOrigid16(20,20,20,85,85,95,85,85,20,20,20,85,55,55,55,85,0,0,0)\n\n\n-- 1\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 100, 106, 93, 54, 124, 110, 100, 15, 100, 115, 107, 146, 76, 115, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(20,20,20,85,55,55,55,85,20,20,20,85,85,95,85,85,0,0,0)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 100, 100, 93, 55, 124, 100, 100, 15, 100, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

