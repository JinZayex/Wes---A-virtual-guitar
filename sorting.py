import numpy as np


def insertionSort(array):
    #print("insertionSort function")
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j+1] = key

    lista = []      
    for i in range(len(array)):
        lista.append(array[i])

    #print(f'1:{lista}')
    return lista

   
"""
            var chord_type = [  [0,4,7],          //00: M (0)*
                                [0,3,7],          //1: m*
                                [0,3,6],          //02: dim*
                                [0,5,7],          //03: sus4 = Suspended Fourth*
                                [0,5,7,10],       //04: 7sus4 = Dominant7, Suspended Fourth*
                                [0,4,7,11],       //05: M7 = Major Seventh*
                                [0,3,7,11],       //06: mMa7 = minor Major Seventh*
                                [0,3,7,10],       //07: m7 = minor Seventh*
                                [0,4,7,10],       //08: m7 = Dominant Seventh*
                                [0,3,6,9],        //09: dim7 = Diminished Seventh*
                                [0,4,8,11],       //10: #5Maj7 = Major Seventh, Raised Fifth*
                                [0,4,8,10],       //11: #57 = Dominant Seventh, Raised Fifth*
                                [0,4,8],          //12: #5 = Majör Raised Fifth*
                                [0,3,6,10],       //13: m7b5 = minor 7th, Flat Fifth*
                                [0,4,6,10],       //14: M7b5 = Major 7th, Flat Fifth*                     
                                [0,4,7,2],        //15: add9 = Major additional Ninth*
                                [0,4,7,11,2],     //16: Maj7(9) = Major Seventh, plus Ninth*
                                [0,4,7,10,2],     //17: 7(9) = Dominant Seventh, plus Ninth*
                                [0,3,7,2],        //18: add9 = minor additional Ninth*
                                [0,3,7,11,2],     //19: m9(Maj7) = minor Major Seventh, plus Ninth*
                                [0,3,7,10,2],     //20: m7(9) = minor Seventh, plus Ninth*
                                [0,4,7,11,6],     //21: Maj7(#11) = Major Seventh, Sharp Eleventh*
                                [0,4,7,11,2,6],   //22: Maj9(#11) = Major Seventh, Sharp Eleventh, plus Ninth*
                                [0,4,7,10,6],     //23: 7(#11) =  Dom. Seventh, Sharp Eleventh*
                                [0,4,7,10,2,6],   //24: 9(#11) =  Dom. Seventh, Sharp Eleventh, plus Ninth*
                                [0,4,7,10,9],     //25: 7(13) =  Dom. Seventh, Thirteenth*
                                [0,4,7,10,2,9],   //26: 9(13) =  Dom. Seventh, Thirteenth, plus Ninth*
                                [0,4,7,10,1],     //27: 7(b9) = Dominant Seventh, plus Flattened Ninth*
                                [0,4,7,10,8],     //28: 7(b13) =  Dom. Seventh, Flattened Thirteenth*
                                [0,4,7,10,1,8],   //29: 7(b13b9) =  Dom. Seventh, Flattened Thirteenth, plus Flattened Ninth*
                                [0,4,7,10,1,5,8], //30: 7(b13b911) =  Dom. Seventh, Flattened Thirteenth plus Flattenet Ninth, plus Eleventh*
                                [0,4,7,10,3],     //31: 7(#9) = Dominant Seventh, plus Sharp Ninth*
                                [0,3,7,10,5],     //32: m7(11) = minor Seventh, plus Eleventh*
                                [0,3,7,10,2,5],   //33: m9(11) = minor Seventh, plus Eleventh, plus Ninth*
                                [0,0,0]];       //34: Dummy
            var chord_str = ["", "m", "dim", "sus4",  "7sus4", "Maj7", "m(Maj7)", "m7", "7", "o7", "Maj7(#5)", "7(#5)", "aug", "0", "7(b5)", "(add9)", "Maj9", "9", "m(add9)", "m9(Maj7)", "m9", "Maj7(#11)", "Maj9(#11)", "7(#11)", "9(#11)", "7(13)", "9(13)", "7(b9)","7(b13)", "7(b9/b13)", "11(b9/b13)", "7(#9)", "m7(11)", "m11", "x"];

            var all_chords = [  // semi-automatically generated from chord_type & chord_str above
                [ "",           [4,7] ],
                [ "m",          [3,7] ],
                [ "dim",        [3,6] ],
                [ "sus4",       [5,7] ],
                [ "7sus4",      [5,7,10] ],
                [ "Maj7",       [4,7,11] ],
                [ "m(Maj7)",    [3,7,11] ],
                [ "m7",         [3,7,10] ],
                [ "7",          [4,7,10] ],
                [ "o7",         [3,6,9] ],
                [ "Maj7(#5)",   [4,8,11] ],
                [ "7(#5)",      [4,8,10] ],
                [ "aug",        [4,8] ],
                [ "0",          [3,6,10] ],
                [ "7(b5)",      [4,6,10] ],
                [ "(add9)",     [4,7,2] ],
                [ "Maj9",       [4,7,11,2] ],
                [ "9",          [4,7,10,2] ],
                [ "m(add9)",    [3,7,2] ],
                [ "m9(Maj7)",   [3,7,11,2] ],
                [ "m9",         [3,7,10,2] ],
                [ "Maj7(#11)",  [4,7,11,6] ],
                [ "Maj9(#11)",  [4,7,11,2,6] ],
                [ "7(#11)",     [4,7,10,6] ],
                [ "9(#11)",     [4,7,10,2,6] ],
                [ "7(13)",      [4,7,10,9] ],
                [ "9(13)",      [4,7,10,2,9] ],
                [ "7(b9)",      [4,7,10,1] ],
                [ "7(b13)",     [4,7,10,8] ],
                [ "7(b9/b13)",  [4,7,10,1,8] ],
                [ "11(b9/b13)", [4,7,10,1,5,8] ],
                [ "7(#9)",      [4,7,10,3] ],
                [ "m7(11)",     [3,7,10,5] ],
                [ "m11",        [3,7,10,2,5] ],
                [ "x", [0,0,0] ]


"""
