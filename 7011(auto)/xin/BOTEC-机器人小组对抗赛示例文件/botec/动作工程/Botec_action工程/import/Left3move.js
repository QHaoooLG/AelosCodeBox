Blockly.Blocks['1632297692509'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297692509",
      "message0": "Left3move",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297692509'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(20,20,20,70,85,95,85,70,20,20,20,70,85,95,85,70,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(80, 45, 100, 90, 93, 54, 124, 90, 120, 165, 100, 110, 107, 146, 77, 100, 128, 71, 0)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(25)\nMOTOmove19(80, 35, 100, 94, 93, 54, 124, 103, 120, 155, 100, 114, 107, 146, 76, 122, 128, 71, 0)\nMOTOwait()\nMOTOsetspeed(23)\nMOTOmove19(80, 35, 100, 96, 93, 54, 122, 104, 120, 155, 100, 103, 97, 126, 86, 113, 128, 71, 0)\nMOTOwait()\nDelayMs(50)\nMOTOrigid16(40,40,40,100,100,100,100,100,40,40,40,100,100,100,100,100,0,0,0)\nMOTOsetspeed(18)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 0)\nMOTOwait()\n";
  return code;
}

