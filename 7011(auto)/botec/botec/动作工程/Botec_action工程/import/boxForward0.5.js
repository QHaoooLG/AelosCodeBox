Blockly.Blocks['1632297581419'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297581419",
      "message0": "boxForward0.5",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297581419'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(100,100,100,65,100,100,100,65,100,100,100,65,100,100,100,65)\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 100, 94, 55, 124, 100, 100, 15, 99, 100, 106, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(100,100,100,85,50,50,50,85,100,100,100,85,50,50,50,85)\nMOTOrigid16(40,40,40,85,80,80,80,75,40,40,40,85,60,60,60,75)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 105, 94, 55, 123, 108, 100, 15, 99, 111, 102, 136, 78, 112, 128, 71, 100)\nMOTOwait()\nDelayMs(50)\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 105, 90, 55, 123, 107, 100, 15, 99, 105, 84, 141, 67, 105, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(40,40,40,85,50,50,50,75,40,40,40,85,80,80,80,75)\nMOTOsetspeed(15)\nMOTOmove19(100, 185, 101, 95, 80, 55, 106, 85, 100, 15, 99, 95, 110, 145, 77, 93, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(40,40,40,85,80,80,80,75,40,40,40,85,50,50,50,75)\nDelayMs(100)\nMOTOsetspeed(25)\nMOTOmove19(100, 185, 101, 95, 80, 55, 106, 80, 100, 15, 99, 95, 107, 145, 77, 93, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 95, 98, 64, 122, 88, 100, 15, 99, 95, 106, 146, 77, 92, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(40,40,40,30,60,60,60,30,40,40,40,30,60,60,60,30)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 100, 94, 55, 123, 98, 100, 15, 99, 100, 106, 145, 77, 102, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 100, 100, 94, 55, 124, 100, 100, 15, 100, 100, 106, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

