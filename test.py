import math
def line_angle(ax,ay,bx,by,cx,cy):
    dx1 = cx - bx
    dy1 = cy - by
    dx2 = ax - bx
    dy2 = ay - by
    angle1 = math.atan2(dy1, dx1)
    angle1 = -int(angle1 * 180 /math.pi)
    if angle1 < 0:
        angle1 = 360+angle1
    angle2 = math.atan2(dy2, dx2)
    angle2 = -int(angle2 * 180 /math.pi)
    if angle2 < 0:
        angle2 = 360 + angle2
    included_angle = angle1 - angle2
    if abs(included_angle) > 180:
        included_angle=included_angle/abs(included_angle)*(360-abs(included_angle))
    else:
        included_angle*=-1
    if included_angle < 0 :
        included_angle += 360 
    return included_angle
print(str(line_angle(836,293,837,267,836,295)))