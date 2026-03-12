"""
transfer_curve.py
-----------------
Transfer Curve (Vgs-Id) 차트를 생성하는 모듈입니다.
Vd(드레인 전압)별로 그룹화된 데이터를 matplotlib으로 플로팅하며,
비교 대상 데이터(Ref)가 있을 경우 동일 파라미터에 대한 곡선을 병치하고 
$R^2$ (R-squared) 일치율 점수를 산출하여 시각화합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.figure import Figure
from scipy.interpolate import interp1d
from sklearn.metrics import r2_score


# 차트 렌더링에 사용될 컬러 팔레트 (최대 20개의 Vd 값 지원, 넘어가면 순환)
_COLORS = [
    "#E63946", "#2196F3", "#2ecc71", "#FF9800", "#9C27B0",
    "#00BCD4", "#FF5722", "#607D8B", "#8BC34A", "#F44336",
    "#3F51B5", "#009688", "#CDDC39", "#795548", "#FFC107",
    "#673AB7", "#03A9F4", "#4CAF50", "#FF5252", "#1DE9B6",
]


def create_transfer_figure(
    grouped_data: dict,
    log_scale: bool = True,
    title: str = "TFT Transfer Curve",
    figsize: tuple = (8, 6),
    xlim: tuple = None,
    ylim: tuple = None,
    ref_grouped: dict = None
) -> Figure:
    """
    Transfer Curve를 나타내는 matplotlib Figure 객체를 생성합니다.
    
    Args:
        grouped_data (dict): Vd를 키로 가지며 x(Vg), y(Id) 넘파이 배열을 지닌 기본 파싱 데이터
        log_scale (bool): Y축을 로그 스케일로 표시할지 여부 (기본값 True)
        title (str): 차트 제목
        figsize (tuple): 생성할 Figure의 가로, 세로 크기 설정 (기본 8x6)
        xlim (tuple): X축 최솟값/최댓값 (min, max). None이면 Auto 스케일
        ylim (tuple): Y축 최솟값/최댓값 (min, max). None이면 Auto 스케일
        ref_grouped (dict): 비교 대상(Ref) 데이터 딕셔너리. None이면 사용 안 함.
        
    Returns:
        Figure: 렌더링이 완료된 matplotlib Figure 객체
    """
    # 1. Figure 및 Subplot(Axes) 생성
    fig, ax = plt.subplots(figsize=figsize, dpi=100)
    
    # 2. 다크 배경 테마 적용
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#2a2a3e")

    # 3. 데이터 순회하며 플로팅 (Vd 값이 작은 순서대로 정렬)
    for i, (vd, data) in enumerate(sorted(grouped_data.items())):
        color = _COLORS[i % len(_COLORS)]
        x = data["x"]
        
        # Transfer Curve는 누설 전류의 흐름을 확인하기 위해 전류값 절댓값 처리
        y = np.abs(data["y"])

        # 범례에 표시할 기본 Vd 레이블 텍스트
        label_base = f"Vd = {_format_val(vd)} V"
        r2_str = ""
        
        # ── 4. 비교 대상 데이터 플로팅 및 R-squared 점수 계산 ──
        if ref_grouped and vd in ref_grouped:
            ref_x = ref_grouped[vd]["x"]
            ref_y = np.abs(ref_grouped[vd]["y"])
            
            # 메인 X축 범위에 맞추어 Ref 데이터 Y축 값을 선형 보간(Linear Interpolation) 적용
            # bounds_error=False, fill_value=np.nan 적용 시 X축 범위를 벗어나는 데이터는 무시
            try:
                f_interp = interp1d(ref_x, ref_y, kind='linear', bounds_error=False, fill_value=np.nan)
                ref_y_interp = f_interp(x)
                
                # NaN 값을 제외한 유효한 범위의 데이터(마스크 배열) 확보
                # 로그 스케일의 경우 0보다 큰 데이터에 한해서만 필터링 수행
                valid_mask = ~np.isnan(ref_y_interp) & (y > 0) if log_scale else ~np.isnan(ref_y_interp)
                
                # 교차/비교 가능한 유효 데이터가 최소 2개 이상일 때 R2 점수 계산
                if np.sum(valid_mask) > 1:
                    r2_val = r2_score(y[valid_mask], ref_y_interp[valid_mask])
                    r2_str = f" [R²: {r2_val:.3f}]"
                    
                # Ref 데이터 오버레이(점선 형태의 반투명 두께 적용)
                if log_scale:
                    ref_mask = ref_y > 0
                    ax.semilogy(ref_x[ref_mask], ref_y[ref_mask], color=color, linewidth=2,
                                linestyle="--", alpha=0.5, label=f"Ref Vd = {_format_val(vd)}")
                else:
                    ax.plot(ref_x, ref_y, color=color, linewidth=2, linestyle="--", 
                            alpha=0.5, label=f"Ref Vd = {_format_val(vd)}")
            except Exception:
                # 보간 에러 발생 시 부드럽게 무시하고 진행
                pass

        # ── 5. 메인 데이터 플로팅 ──
        if log_scale:
            # 0 이하의 값은 로그 스케일에 그릴 수 없으므로 마스킹하여 제거
            mask = y > 0
            ax.semilogy(x[mask], y[mask], color=color, linewidth=2,
                        label=label_base + r2_str, marker="o",
                        markersize=3, markeredgewidth=0)
        else:
            # 일반 선형 스케일 플로팅
            ax.plot(x, y, color=color, linewidth=2,
                    label=label_base + r2_str, marker="o",
                    markersize=3, markeredgewidth=0)

    # 6. 축 스타일 및 커스텀 한계 범위 지정
    _style_axes(ax, log_scale)

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xlabel("Vgs (V)", color="white", fontsize=12, labelpad=8)
    ax.set_ylabel("|Id| (A)" if log_scale else "Id (A)", color="white", fontsize=12, labelpad=8)
    ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=12)

    # 7. 범례 박스 스타일 적용
    legend = ax.legend(
        loc="best", fontsize=9, framealpha=0.3,
        facecolor="#1e1e2e", edgecolor="#555577", labelcolor="white"
    )

    # 레이아웃 간격 삐쳐나옴 대비 최적화
    plt.tight_layout(pad=1.5)
    return fig


def _format_val(v: float) -> str:
    """
    소수점이 ".0"으로 끝나는 경우 정수형(str)으로 표시하고,
    그 외의 경우 소수 셋업 자리까지 유효숫자로 처리하여 표시합니다.
    """
    if v == int(v):
        return str(int(v))
    return f"{v:.3g}"


def _style_axes(ax, log_scale: bool):
    """
    차트 축과 그리드 선에 다크 테마 색상 및 톤 스타일링을 공통 적용합니다.
    """
    ax.tick_params(colors="white", labelsize=9)
    ax.spines["bottom"].set_color("#555577")
    ax.spines["left"].set_color("#555577")
    ax.spines["top"].set_color("#555577")
    ax.spines["right"].set_color("#555577")
    
    # 주 그리드 라인 설정
    ax.grid(True, which="major", linestyle="--", alpha=0.3, color="#aaaacc")
    
    # 로그 스케일 시 서브 그리드 라인(미세 격자) 추가
    if log_scale:
        ax.grid(True, which="minor", linestyle=":", alpha=0.15, color="#aaaacc")
