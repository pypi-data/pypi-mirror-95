define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function( NumpyPageRender ) {

    'use strict';
    /**
     * @class NpDstackHstackVstackPageRender
     * @constructor
     */
    var NpDstackHstackVstackPageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyAxisArray, numpyIndexValueArray, numpyEnumRenderEditorFuncType, 
                numpyTrueFalseArray, numpyRavelOrderArray } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyAxisArray = numpyAxisArray;
        this.numpyIndexValueArray = numpyIndexValueArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;
        this.numpyTrueFalseArray = numpyTrueFalseArray
        this.numpyRavelOrderArray = numpyRavelOrderArray;
        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
     */
    NpDstackHstackVstackPageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
     * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
     */
    NpDstackHstackVstackPageRender.prototype.pageRender = function() {
        this.rootTagSelector = this.getMainPageSelector();
        var numpyPageRenderThis = this;
        const {  PARAM_INPUT_EDITOR_TYPE, PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(this.numpyStateGenerator.getState('paramData'));
        var tabTitle = 'Input Stacking Array';
        var tabBlockArray = [
            {
                tabNumber: 1
                , btnText: '1개 배열 합치기'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [stateParamNameStrArray[0]]
                    , paramNameStrArray: [ '배열' ]
                    , placeHolderArray: [ '변수 입력'  ]
                }
          
            },
            {
                tabNumber: 2
                , btnText: '2개 배열 합치기'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ stateParamNameStrArray[1], stateParamNameStrArray[2]]
                    , paramNameStrArray: [ '배열',  '배열'  ]
                    , placeHolderArray: [ '변수 입력', '변수 입력' ]
                }
               
            },
            {
                tabNumber: 3
                , btnText: '3개 배열 합치기'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray:  [ stateParamNameStrArray[3], stateParamNameStrArray[4], stateParamNameStrArray[5]]
                    , paramNameStrArray: [ '배열',  '배열', '배열'  ]
                    , placeHolderArray: [ '변수 입력', '변수 입력', '변수 입력' ]
                }
           
            },
            {
                tabNumber: 4
                , btnText: 'N개 배열 합치기'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE
                    , stateParamNameStrOrStrArray:  stateParamNameStrArray[6]
                }
            }
        ];
        var tabDataObj = {
            tabTitle,
            tabBlockArray
        }

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamTabBlock(tabDataObj);
        
         /** 옵션 창 */
        this.renderAdditionalOptionContainer();
        this.renderReturnVarBlock();

        this.renderPostfixCode();
    }

    return NpDstackHstackVstackPageRender;
});
