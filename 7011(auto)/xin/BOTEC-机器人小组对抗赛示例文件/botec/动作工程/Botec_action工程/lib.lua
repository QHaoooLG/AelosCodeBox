
function ReadGpio(gpio)
  status, table = sensorReq("SensorInput", { gpio }, 3600)
  if status ~= 0 then
    return -255
  end
  return table[1]
end

function getDistance()
  local volt = ReadGpio(5)
  if (volt == -255) then
    return 0
  else
    local distance = 1.35569260506789e-06 * volt^4 - 0.000625977766708382 * volt^3 + 0.10628603694879 * volt^2 - 8.23675807124173 * volt + 289.50385704274
    return math.floor(distance + 0.5)
  end
end

function WriteGpio(gpio, status)
  sensorReq("IOout", { gpio, status }, 25)
end

function ReadGeomagneticSensor()
  status, table = sensorReq("SensorInput", { 8 }, 3600)
  if status ~= 0 then
    return -255
  end
  return table[1]
end

function ReadColours(r, g, b)
  status, table = sensorReq("ImageIdent", { {r, g, b} }, 3600)
  if status ~= 0 then
    return status, {}
  end
  return status, table[1]
end

function ReadColoursInDelta(r, g, b, delta)
  status, table = sensorReq("ColorRange", { {r, g, b}, delta }, 3600)
  if status ~= 0 then
    return status, {}
  end
  return status, table[1]
end
  
function IsColourOfRGB(r, g, b)
  status, table = ReadColours(r, g, b)
  if status ~= 0 then
    return false
  end
  if table[3] < 1 then
    return false
  end
  return true
end

function IsColourOfRGBInDelta(r, g, b, delta)
  status, table = ReadColoursInDelta(r, g, b, delta)
  if status ~= 0 then
    return false
  end
  if table[3] < 1 then
    return false
  end
  return true
end

function IsColourOfRGBInPosition(r, g, b, positon)
  status, table = ReadColours(r, g, b)
  if status ~= 0 then
    return false
  end
  if table[3] < 1 then
    return false
  end
  result = table[4]
  if result == 0x01 and positon == "left" then
    return true
  end
  if result == 0x02 and positon == "center" then
    return true
  end
  if result == 0x03 and positon == 'right' then
    return true
  end
  return false
end

function getColourOfAxis(r, g, b, axis)
  status, table = ReadColours(r, g, b)
  if status ~= 0 then
    return 0
  end
  if axis == 'X' then
    return table[1]
  end
  if axis == 'Y' then
    return table[2]
  end
  return 0
end

function getColourOfParameter(r, g, b, name)
  status, table = ReadColours(r, g, b)
  if status ~= 0 then
    return 0
  end
  if name == 'X' then
    return table[1]
  end
  if name == 'Y' then
    return table[2]
  end
  if name == 'W' then
    return table[5]
  end
  if name == 'H' then
    return table[6]
  end
  return 0
end

function getColourOfAreaSize(r, g, b)
  status, table = ReadColours(r, g, b)
  if status ~= 0 then
    return 0
  end
  return table[3]
end

function ReadFaceData(time)
  status = 0x01
  table = {}
  for i = time, 1, -1 do
    status, table = sensorReq("FaceReg", { 2 }, 3000)
    if status == 0x00 and table[1] ~= nil and  table[1][1] ~= 0x00 then
      break
    end
  end
  if status ~= 0 then
    return status, {}
  end
  return status, table[1]
end

function IsPersonIncamera(time, sex, age, emotion)
  sexs = {
    ['male'] = 0x01,
    ['female'] = 0x02,
  }
  ages = {
    ['child'] = 0x01,
    ['teen'] = 0x02,
    ['youth'] = 0x03,
    ['middle-age'] = 0x04,
    ['elder'] = 0x05,
  }
  emotions = {
    ['sadness'] = 0x02,
    ['neutral'] = 0x01,
    ['contempt'] = 0x08,
    ['disgust'] = 0x04,
    ['anger'] = 0x05,
    ['surprise'] = 0x06,
    ['fear'] = 0x07,
    ['happiness'] = 0x03,
  }
  status, table = ReadFaceData(time)
  if status ~= 0 or table[1] == 0x00 then
    return false
  end
  if sex == 'any' and age == 'any' and emotion == 'any' then
    return true
  end
  if sex == 'any' and age == 'any' then
    if table[3] == emotions[emotion] then
      return true
    end
    return false
  end
  if sex == 'any' and emotion == 'any' then
    if table[2] == ages[age] then
      return true
    end
    return false
  end
  if age == 'any' and emotion == 'any' then
    if table[1] == sexs[sex] then
      return true
    end
    return false
  end
  if sex == 'any' then
    if table[2] == ages[age] and table[3] == emotions[emotion] then
      return true
    end
    return false
  end
  if age == 'any' then
    if table[1] == sexs[sex] and table[3] == emotions[emotion] then
      return true
    end
    return false
  end
  if emotion == 'any' then
    if table[1] == sexs[sex] and table[2] == ages[age] then
      return true
    end
    return false
  end
  if table[1] == sexs[sex] and table[2] == ages[age] and table[3] == emotions[emotion] then
    return true
  end
  return false
end

function IsFaceIncamera(time)
  status, table = ReadFaceData(time)
  if status ~= 0 or table[1] == 0x00 then
    return false
  end
  if table[1] ~= 0x00 then
    return true
  end
  return false
end

function IdentifyQRCode()
  status, table = sensorReq("TagReg", { 0 }, 3600)
  if status ~= 0 or computedNegativeNumber(table[1][1]) == -1 then
    return {-1, 1000, 1000, 1000}
  end
  return table[1]
end

function ReadLabelContent()
  table = IdentifyQRCode()
  return table[1]
end

function ReadLabelContentX(Xmin, Xmax)
  table = IdentifyQRCode()
  if table[2] >= Xmin and table[2] <= Xmax then
    return table[1]
  end
  return 1000
end

function ReadLabelContentY(Ymin, Ymax)
  table = IdentifyQRCode()
  local value = computedNegativeNumber(table[3])
  if value >= Ymin and value <= Ymax then
    return table[1]
  end
  return 1000
end

function ReadDistance(axis)
  table = IdentifyQRCode()
  if axis == 'X' then
    return table[2]
  end
  if axis == 'Y' then
    return computedNegativeNumber(table[3])
  end
end

function ReadLabelContentYAW()
  table = IdentifyQRCode()
  return computedNegativeNumber(table[4])
end

function computedNegativeNumber(number)
  if number >= (65536 / 2) then
    return number - 65536
  else
    return number
  end
end

function IsSexInCase(time, sex)
  sexs = {
    ['male'] = 0x01,
    ['female'] = 0x02,
  }
  status, table = ReadFaceData(time)
  if status ~= 0 or table[1] == 0x00 then
    return false
  end
  if table[1] == sexs[sex] then
    return true
  end
  return false
end

function IsAgeInRange(time, age)
  ages = {
    ['child'] = 0x01,
    ['teen'] = 0x02,
    ['youth'] = 0x03,
    ['middle-age'] = 0x04,
    ['elder'] = 0x05,
  }
  status, table = ReadFaceData(time)
  if status ~= 0 or table[2] == 0x00 then
    return false
  end
  if table[2] == ages[age] then
    return true
  end
  return false
end

function IsEmotionInCase(time, emotion)
  emotions = {
    ['sadness'] = 0x02,
    ['neutral'] = 0x01,
    ['contempt'] = 0x08,
    ['disgust'] = 0x04,
    ['anger'] = 0x05,
    ['surprise'] = 0x06,
    ['fear'] = 0x07,
    ['happiness'] = 0x03,
  }
  status, table = ReadFaceData(time)
  if status ~= 0 or table[3] == 0x00 then
    return false
  end
  if table[3] == emotions[emotion] then
    return true
  end
  return false
end

function ReadCustomColoursByHSV(hmin, hmax, smin, smax, vmin, vmax)
  status, table = sensorReq("CustomColor", { {hmin, hmax, smin, smax, vmin, vmax} }, 3600)
  if status ~= 0 then
    return status, {}
  end
  return status, table[1]
end

function IsColourOfHSV(hmin, hmax, smin, smax, vmin, vmax)
  status, table = ReadCustomColoursByHSV(hmin, hmax, smin, smax, vmin, vmax)
  if status ~= 0 then
    return false
  end
  if table[3] < 1 then
    return false
  end
  return true
end

function IsColourOfHSVInPosition(hmin, hmax, smin, smax, vmin, vmax, positon)
  status, table = ReadCustomColoursByHSV(hmin, hmax, smin, smax, vmin, vmax)
  if status ~= 0 then
    return false
  end
  if table[3] < 1 then
    return false
  end
  result = table[4]
  if result == 0x01 and positon == "left" then
    return true
  end
  if result == 0x02 and positon == "center" then
    return true
  end
  if result == 0x03 and positon == 'right' then
    return true
  end
  return false
end

function getColourOfAxisByHSV(hmin, hmax, smin, smax, vmin, vmax, axis)
  status, table = ReadCustomColoursByHSV(hmin, hmax, smin, smax, vmin, vmax)
  if status ~= 0 then
    return 0
  end
  if axis == 'X' then
    return table[1]
  end
  if axis == 'Y' then
    return table[2]
  end
  return 0
end

function getColourOfParameterByHSV(hmin, hmax, smin, smax, vmin, vmax, name)
  status, table = ReadCustomColoursByHSV(hmin, hmax, smin, smax, vmin, vmax)
  if status ~= 0 then
    return 0
  end
  if name == 'X' then
    return table[1]
  end
  if name == 'Y' then
    return table[2]
  end
  if name == 'W' then
    return table[5]
  end
  if name == 'H' then
    return table[6]
  end
  return 0
end

function getColourOfAreaSizeByHSV(hmin, hmax, smin, smax, vmin, vmax)
  status, table = ReadCustomColoursByHSV(hmin, hmax, smin, smax, vmin, vmax)
  if status ~= 0 then
    return 0
  end
  return table[3]
end

function fast_forward_step(cnt)
  MOTOrigid16(25, 25, 25, 55, 65, 90, 80, 50, 25, 25, 25, 55, 65, 90, 80, 50)
  MOTOdamp16(15, 15, 15, 15, 60, 50, 15, 15, 15, 15, 15, 15, 60, 50, 15, 15)

  MOTOsetspeed(45)
  MOTOmove16(80, 30, 100, 99, 93, 54, 121, 90, 120, 170, 100, 98, 107, 146, 76, 95)
  MOTOwait()

  MOTOsetspeed(58)
  MOTOmove16(80, 30, 80, 99, 115, 99, 97, 100, 120, 170, 80, 101, 109, 134, 92, 94)
  MOTOwait()

  MOTOsetspeed(65)
  MOTOmove16(80, 30, 80, 99, 110, 74, 120, 100, 120, 170, 80, 101, 114, 137, 92, 100)
  MOTOwait()

  MOTOsetspeed(73)
  MOTOmove16(80, 30, 80, 99, 110, 61, 125, 104, 120, 170, 80, 101, 100, 127, 95, 100)
  MOTOwait()

  MOTOsetspeed(73)
  MOTOmove16(80, 30, 120, 99, 91, 66, 108, 102, 120, 170, 120, 101, 85, 101, 103, 100)
  MOTOwait()

  MOTOsetspeed(73)
  MOTOmove16(80, 30, 120, 99, 86, 63, 109, 100, 120, 170, 120, 101, 90, 126, 80, 100)
  MOTOwait()

  MOTOsetspeed(73)
  MOTOmove16(80, 30, 120, 99, 100, 73, 105, 100, 120, 170, 120, 101, 90, 139, 75, 94)
  MOTOwait()

  for var = 1, cnt, 1 do
    MOTOsetspeed(70)
    MOTOmove16(80, 30, 80, 99, 115, 99, 97, 100, 120, 170, 80, 101, 109, 134, 90, 98)
    MOTOwait()

    MOTOsetspeed(73)
    MOTOmove16(80, 30, 80, 99, 110, 74, 120, 100, 120, 170, 80, 101, 114, 137, 90, 100)
    MOTOwait()

    MOTOsetspeed(73)
    MOTOmove16(80, 30, 80, 99, 110, 61, 125, 104, 120, 170, 80, 101, 100, 127, 95, 100)
    MOTOwait()

    MOTOsetspeed(70)
    MOTOmove16(80, 30, 120, 99, 91, 66, 110, 102, 120, 170, 120, 101, 85, 101, 103, 100)
    MOTOwait()

    MOTOsetspeed(73)
    MOTOmove16(80, 30, 120, 99, 86, 63, 110, 100, 120, 170, 120, 101, 90, 126, 80, 100)
    MOTOwait()

    MOTOsetspeed(73)
    MOTOmove16(80, 30, 120, 99, 100, 73, 105, 100, 120, 170, 120, 101, 90, 139, 75, 96)
    MOTOwait()
  end

  MOTOsetspeed(65)
  MOTOmove16(80, 30, 80, 96, 95, 70, 110, 100, 120, 170, 80, 102, 109, 146, 75, 96)
  MOTOwait()
  MOTOsetspeed(45)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
  MOTOwait()
end

function fast_forward_smooth_step(cnt)
  MOTOrigid16(25, 25, 10, 55, 65, 90, 80, 50, 25, 25, 10, 55, 65, 90, 80, 50)
  MOTOdamp16(15, 15, 15, 15, 60, 50, 15, 15, 15, 15, 15, 15, 60, 50, 15, 15)

  MOTOsetspeed(45)
  MOTOmove16(80, 30, 100, 99, 93, 54, 122, 90, 120, 170, 100, 98, 107, 146, 75, 95)
  MOTOwait()

  MOTOsetspeed(60)
  MOTOmove16(80, 30, 80, 99, 115, 99, 103, 100, 120, 170, 80, 101, 109, 134, 91, 94)
  MOTOwait()

  MOTOsetspeed(70)
  MOTOmove16(80, 30, 80, 99, 110, 74, 121, 100, 120, 170, 80, 101, 114, 137, 91, 100)
  MOTOwait()

  MOTOsetspeed(80)
  MOTOmove16(80, 30, 80, 99, 110, 61, 126, 104, 120, 170, 80, 101, 100, 127, 94, 100)
  MOTOwait()

  MOTOsetspeed(80)
  MOTOmove16(80, 30, 120, 99, 91, 66, 109, 102, 120, 170, 120, 101, 85, 101, 97, 100)
  MOTOwait()

  MOTOsetspeed(80)
  MOTOmove16(80, 30, 120, 99, 86, 63, 110, 100, 120, 170, 120, 101, 90, 126, 79, 100)
  MOTOwait()

  MOTOsetspeed(80)
  MOTOmove16(80, 30, 120, 99, 100, 73, 106, 100, 120, 170, 120, 101, 90, 139, 74, 94)
  MOTOwait()

  for var = 1, cnt, 1 do
    MOTOsetspeed(75)
    MOTOmove16(80, 30, 80, 99, 115, 99, 103, 100, 120, 170, 80, 101, 109, 134, 89, 98)
    MOTOwait()

    MOTOsetspeed(80)
    MOTOmove16(80, 30, 80, 99, 110, 74, 121, 100, 120, 170, 80, 101, 114, 137, 89, 100)
    MOTOwait()

    MOTOsetspeed(80)
    MOTOmove16(80, 30, 80, 99, 110, 61, 126, 104, 120, 170, 80, 101, 100, 127, 94, 100)
    MOTOwait()

    MOTOsetspeed(75)
    MOTOmove16(80, 30, 120, 99, 91, 66, 111, 102, 120, 170, 120, 101, 85, 101, 97, 100)
    MOTOwait()

    MOTOsetspeed(80)
    MOTOmove16(80, 30, 120, 99, 86, 63, 111, 100, 120, 170, 120, 101, 90, 126, 79, 100)
    MOTOwait()

    MOTOsetspeed(80)
    MOTOmove16(80, 30, 120, 99, 100, 73, 106, 100, 120, 170, 120, 101, 90, 139, 74, 96)
    MOTOwait()
  end

  MOTOsetspeed(65)
  MOTOmove16(80, 30, 80, 96, 95, 70, 110, 100, 120, 170, 80, 102, 109, 146, 75, 96)
  MOTOwait()
  MOTOsetspeed(45)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
  MOTOwait()
end

function fast_backward_step(cnt)
  MOTOrigid16(25, 25, 25, 55, 65, 90, 80, 50, 25, 25, 25, 55, 65, 90, 80, 50)
  MOTOdamp16(15, 15, 15, 15, 50, 30, 15, 15, 15, 15, 15, 15, 50, 30, 15, 15)
  MOTOsetspeed(45)
  MOTOmove16(80, 30, 100, 99, 93, 55, 124, 89, 120, 170, 100, 98, 107, 145, 78, 93)
  MOTOwait()
  MOTOsetspeed(58)
  MOTOmove16(80, 30, 120, 99, 113, 100, 99, 100, 120, 170, 120, 101, 100, 141, 77, 95)
  MOTOwait()
  MOTOsetspeed(65)
  MOTOmove16(80, 30, 120, 99, 95, 70, 109, 100, 120, 170, 120, 101, 98, 141, 75, 99)
  MOTOwait()
  MOTOsetspeed(78)
  MOTOmove16(80, 30, 120, 99, 90, 60, 117, 105, 120, 170, 120, 101, 95, 118, 91, 99)
  MOTOwait()
  MOTOsetspeed(78)
  MOTOmove16(80, 30, 80, 99, 95, 59, 123, 101, 120, 170, 80, 101, 87, 100, 101, 100)
  MOTOwait()
  MOTOsetspeed(78)
  MOTOmove16(80, 30, 80, 99, 97, 59, 123, 101, 120, 170, 80, 101, 105, 130, 91, 100)
  MOTOwait()
  MOTOsetspeed(78)
  MOTOmove16(80, 30, 80, 99, 102, 82, 109, 101, 120, 170, 80, 101, 110, 140, 83, 95)
  MOTOwait()

  for var = 1, cnt, 1 do
    MOTOsetspeed(78)
    MOTOmove16(80, 30, 120, 99, 113, 100, 99, 100, 120, 170, 120, 101, 100, 141, 77, 99)
    MOTOwait()
    MOTOsetspeed(78)
    MOTOmove16(80, 30, 120, 99, 95, 70, 109, 100, 120, 170, 120, 101, 100, 141, 77, 99)
    MOTOwait()

    MOTOsetspeed(78)
    MOTOmove16(80, 30, 120, 99, 90, 60, 117, 105, 120, 170, 120, 101, 95, 118, 91, 99)
    MOTOwait()

    MOTOsetspeed(78)
    MOTOmove16(80, 30, 80, 99, 100, 59, 123, 101, 120, 170, 80, 101, 87, 100, 101, 100)
    MOTOwait()

    MOTOsetspeed(78)
    MOTOmove16(80, 30, 80, 99, 100, 59, 123, 101, 120, 170, 80, 101, 105, 130, 91, 100)
    MOTOwait()

    MOTOsetspeed(78)
    MOTOmove16(80, 30, 80, 99, 105, 82, 109, 101, 120, 170, 80, 101, 110, 140, 83, 95)
    MOTOwait()
  end

  MOTOsetspeed(70)
  MOTOmove16(80, 30, 120, 97, 113, 100, 99, 100, 120, 170, 120, 101, 103, 145, 78, 96)
  MOTOwait()
  MOTOsetspeed(70)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 97, 120, 170, 100, 100, 107, 145, 76, 103)
  MOTOwait()
  MOTOsetspeed(30)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
  MOTOwait()
end

function fast_backward_smooth_step(cnt)
  MOTOrigid16(25, 25, 10, 55, 65, 90, 80, 50, 25, 25, 10, 55, 65, 90, 80, 50)
  MOTOdamp16(15, 15, 15, 15, 50, 30, 15, 15, 15, 15, 15, 15, 50, 30, 15, 15)
  MOTOsetspeed(65)
  MOTOmove16(80, 30, 100, 99, 93, 55, 125, 92, 120, 170, 100, 98, 107, 145, 77, 95)
  MOTOwait()

  for var = 1, cnt, 1 do
    MOTOsetspeed(100)
    MOTOmove16(80, 30, 120, 99, 113, 100, 100, 100, 120, 170, 120, 101, 100, 142, 75, 99)
    MOTOwait()

    MOTOsetspeed(100)
    MOTOmove16(80, 30, 120, 99, 95, 70, 110, 100, 120, 170, 120, 101, 95, 138, 75, 99)
    MOTOwait()

    MOTOsetspeed(100)
    MOTOmove16(80, 30, 120, 99, 90, 65, 112, 105, 120, 170, 120, 101, 95, 118, 90, 99)
    MOTOwait()

    MOTOsetspeed(110)
    MOTOmove16(80, 30, 80, 99, 100, 58, 125, 101, 120, 170, 80, 101, 87, 100, 100, 100)
    MOTOwait()

    MOTOsetspeed(100)
    MOTOmove16(80, 30, 80, 99, 105, 62, 125, 101, 120, 170, 80, 101, 105, 130, 90, 100)
    MOTOwait()

    MOTOsetspeed(100)
    MOTOmove16(80, 30, 80, 99, 105, 82, 110, 101, 120, 170, 80, 101, 110, 135, 88, 95)
    MOTOwait()
  end

  MOTOsetspeed(70)
  MOTOmove16(80, 30, 120, 97, 113, 100, 99, 100, 120, 170, 120, 101, 103, 145, 78, 96)
  MOTOwait()
  MOTOsetspeed(70)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 97, 120, 170, 100, 100, 107, 145, 76, 103)
  MOTOwait()
  MOTOsetspeed(30)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
  MOTOwait()
end

function slow_forward_step(cnt)
  MOTOrigid16(20, 20, 20, 65, 65, 65, 65, 65, 20, 20, 20, 65, 65, 65, 65, 65)
  MOTOsetspeed(8)
  MOTOmove16(80, 35, 100, 90, 91, 48, 129, 88, 120, 165, 100, 94, 107, 146, 76, 92)
  MOTOwait()
  MOTOsetspeed(30)
  MOTOmove16(80, 35, 90, 86, 105, 85, 100, 90, 120, 165, 90, 94, 107, 146, 78, 87)
  MOTOwait()

  for var = 1, cnt, 1 do
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 90, 86, 113, 37, 156, 90, 120, 165, 90, 94, 107, 146, 77, 90)
    MOTOwait()
    MOTOsetspeed(10)
    MOTOmove16(80, 35, 90, 107, 100, 56, 124, 110, 120, 165, 90, 112, 129, 155, 93, 110)
    MOTOwait()
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 110, 106, 93, 54, 123, 111, 120, 165, 110, 114, 90, 105, 100, 110)
    MOTOwait()
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 110, 106, 93, 54, 123, 110, 120, 165, 110, 114, 87, 163, 44, 110)
    MOTOwait()
    MOTOsetspeed(10)
    MOTOmove16(80, 35, 110, 88, 71, 45, 107, 90, 120, 165, 110, 93, 100, 144, 76, 90)
    MOTOwait()
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 90, 86, 110, 95, 100, 90, 120, 165, 90, 94, 107, 146, 77, 89)
    MOTOwait()
  end

  MOTOrigid16(20, 20, 20, 45, 65, 65, 65, 45, 20, 20, 20, 45, 65, 65, 65, 45)
  MOTOsetspeed(20)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
  MOTOwait()
end

function slow_backward_step(cnt)
  MOTOrigid16(20, 20, 20, 65, 65, 65, 65, 65, 20, 20, 20, 65, 65, 65, 65, 65)
  MOTOsetspeed(8)
  MOTOmove16(80, 35, 100, 90, 91, 48, 129, 88, 120, 165, 100, 94, 107, 146, 76, 92)
  MOTOwait()
  MOTOsetspeed(30)
  MOTOmove16(80, 35, 90, 86, 105, 85, 105, 90, 120, 165, 90, 94, 107, 146, 78, 87)
  MOTOwait()

  for var = 1, cnt, 1 do
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 90, 88, 71, 53, 104, 85, 120, 165, 90, 93, 100, 144, 72, 91)
    MOTOwait()
    MOTOsetspeed(10)
    MOTOmove16(80, 35, 90, 106, 93, 53, 127, 110, 120, 165, 90, 114, 87, 163, 42, 110)
    MOTOwait()
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 110, 106, 93, 53, 125, 112, 120, 165, 110, 114, 90, 105, 96, 110)
    MOTOwait()
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 110, 107, 100, 56, 128, 109, 120, 165, 110, 112, 129, 147, 96, 115)
    MOTOwait()
    MOTOsetspeed(10)
    MOTOmove16(80, 35, 110, 86, 113, 37, 158, 90, 120, 165, 110, 94, 107, 147, 73, 90)
    MOTOwait()
    MOTOsetspeed(30)
    MOTOmove16(80, 35, 90, 86, 110, 95, 104, 90, 120, 165, 90, 94, 107, 147, 75, 88)
    MOTOwait()
  end

  MOTOsetspeed(20)
  MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
  MOTOwait()
end

function left_move_step(cnt)
  MOTOrigid16(20, 20, 20, 65, 85, 95, 85, 35, 20, 20, 20, 65, 55, 55, 55, 35)

  for var = 1, cnt, 1 do
    MOTOsetspeed(65)
    MOTOmove16(80, 40, 100, 85, 112, 95, 105, 90, 120, 160, 100, 110, 107, 146, 76, 100)
    MOTOwait()
    DelayMs(50)
    MOTOsetspeed(75)
    MOTOmove16(80, 30, 100, 95, 93, 53, 121, 105, 120, 155, 100, 120, 116, 160, 68, 130)
    MOTOwait()
    MOTOsetspeed(65)
    MOTOmove16(80, 30, 100, 100, 93, 54, 124, 98, 120, 170, 100, 103, 107, 146, 76, 105)
    MOTOwait()
    MOTOsetspeed(20)
    MOTOmove19(80, 30, 100, 100, 93, 55, 124, 95, 120, 170, 100, 100, 107, 145, 76, 105, 128, 71, 100)
    MOTOwait()
    DelayMs(50)
    MOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 100)
    MOTOwait()
    DelayMs(800)
  end
end

function right_move_step(cnt)
  MOTOrigid16(20, 20, 20, 65, 55, 55, 55, 35, 20, 20, 20, 65, 85, 95, 85, 35)

  for var = 1, cnt, 1 do
    MOTOsetspeed(65)
    MOTOmove16(80, 40, 100, 90, 93, 54, 124, 100, 120, 160, 100, 115, 88, 105, 95, 110)
    MOTOwait()
    DelayMs(50)
    MOTOsetspeed(75)
    MOTOmove16(80, 45, 100, 80, 84, 40, 132, 70, 120, 170, 100, 105, 107, 147, 79, 95)
    MOTOwait()
    MOTOsetspeed(65)
    MOTOmove16(80, 30, 100, 97, 93, 54, 124, 95, 120, 170, 100, 100, 107, 146, 76, 102)
    MOTOwait()
    MOTOsetspeed(20)
    MOTOmove19(80, 30, 100, 100, 93, 55, 124, 95, 120, 170, 100, 100, 107, 145, 76, 105, 128, 71, 100)
    MOTOwait()
    DelayMs(50)
    MOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 100)
    MOTOwait()
    DelayMs(800)
  end
end

function left_turn_step(cnt)
  MOTOrigid16(20, 20, 20, 75, 65, 65, 65, 65, 30, 20, 20, 65, 75, 65, 65, 65)

  for var = 1, cnt, 1 do
    MOTOsetspeed(24)
    MOTOmove16(80, 30, 115, 95, 63, 55, 94, 95, 120, 170, 115, 105, 77, 145, 46, 105)
    MOTOwait()
    DelayMs(50)
    MOTOsetspeed(30)
    MOTOmove16(80, 30, 115, 95, 63, 55, 94, 93, 120, 170, 115, 105, 77, 145, 46, 107)
    MOTOwait()
    DelayMs(50)
    MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
    MOTOwait()
    DelayMs(800)
  end
end

function right_turn_step(cnt)
  MOTOrigid16(20, 20, 20, 75, 65, 65, 65, 65, 20, 20, 20, 75, 65, 65, 65, 65)

  for var = 1, cnt, 1 do
    MOTOsetspeed(24)
    MOTOmove16(80, 30, 85, 95, 123, 55, 154, 95, 120, 170, 85, 105, 137, 145, 106, 105)
    MOTOwait()
    DelayMs(50)
    MOTOsetspeed(30)
    MOTOmove16(80, 30, 85, 95, 123, 55, 154, 93, 120, 170, 85, 105, 137, 145, 106, 107)
    MOTOwait()
    DelayMs(50)
    MOTOmove16(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100)
    MOTOwait()
    DelayMs(800)
  end
end

function IsVoiceCommand(target)
  local i = ReadGpio(3)
  local delta = 4
  if i >= target - delta and i <= target + delta then
    return true
  end
  return false
end

function ReadInclinationAngle(axis)
  local Accel = Get_ACC();
  local accelX = Accel[1];
  local accelZ = Accel[2];
  local accelY = Accel[3];
  if axis == 'X' then
    local pitch = 180 * math.atan(accelX, math.sqrt(accelY * accelY + accelZ * accelZ)) / math.pi;
    return pitch;
  end
  if axis == 'Y' then
    local roll = 180 * math.atan(accelY, math.sqrt(accelX * accelX + accelZ * accelZ)) / math.pi;
    return roll;
  end
end

function compareInclinationAngleRange(axis, angle_1, angle_2)
  local angle = ReadInclinationAngle(axis);
  if angle_1 > angle_2 then
    return angle <= angle_1 and angle >= angle_2
  end
  return angle >= angle_1 and angle <= angle_2
end

function IdentifyGestures(port, target)
  local gpio = ReadGpio(port)
  local delta = 4
  if gpio >= target - delta and gpio <= target + delta then
    return true
  end
    return false
end
